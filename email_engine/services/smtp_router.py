# email_engine/services/smtp_router.py - COMPLETE VERSION
import random
import logging
from collections import defaultdict
from django.utils import timezone
from django.core.cache import cache
from ..models import SMTPConfig

logger = logging.getLogger(__name__)


class SMTPRouter:
    """Enterprise SMTP router with load balancing, health checks, and rotation"""
    
    @staticmethod
    def reset_counters(config):
        """Reset daily/hourly counters if needed"""
        now = timezone.now()
        needs_save = False
        
        if now.date() > config.last_reset_at.date():
            config.sent_today = 0
            needs_save = True
        
        if now.hour != config.last_reset_at.hour or now.day != config.last_reset_at.day:
            config.sent_this_hour = 0
            needs_save = True
        
        if needs_save:
            config.last_reset_at = now
            config.save(update_fields=['sent_today', 'sent_this_hour', 'last_reset_at'])
    
    @staticmethod
    def can_send(config):
        """Check if SMTP can send based on rate limits and health"""
        SMTPRouter.reset_counters(config)
        
        if not config.is_active:
            return False
        
        if config.health_score < 20:
            return False
        
        if config.daily_limit > 0 and config.sent_today >= config.daily_limit:
            logger.info(f"SMTP {config.host} hit daily limit ({config.sent_today}/{config.daily_limit})")
            return False
        
        if config.hourly_limit > 0 and config.sent_this_hour >= config.hourly_limit:
            logger.info(f"SMTP {config.host} hit hourly limit ({config.sent_this_hour}/{config.hourly_limit})")
            return False
        
        return True
    
    @staticmethod
    def get_available_smtps(organization, email_type='campaign', priority=5):
        """Get all available SMTPs for the organization"""
        if not organization:
            return []
        
        smtps = list(organization.smtpconfig_set.filter(is_active=True))
        available = [s for s in smtps if SMTPRouter.can_send(s)]
        
        # For OTP/high priority, filter by type and health
        if priority >= 8 or email_type == 'otp':
            available = [s for s in available if s.health_score >= 70]
        
        return available
    
    @staticmethod
    def select_smtp(organization, email_type='campaign', priority=5):
        """
        Select best SMTP with load balancing and rotation.
        Returns the selected SMTP config.
        """
        available = SMTPRouter.get_available_smtps(organization, email_type, priority)
        
        if not available:
            logger.warning(f"No available SMTP for org {organization.name}")
            return None
        
        # Get cache key for round-robin tracking
        cache_key = f"smtp_round_robin_{organization.id}_{email_type}"
        last_index = cache.get(cache_key, 0)
        
        # Group by priority
        by_priority = defaultdict(list)
        for smtp in available:
            by_priority[smtp.priority].append(smtp)
        
        # Shuffle each priority group for load balancing
        for p in by_priority:
            random.shuffle(by_priority[p])
        
        # Flatten: lower priority numbers come first
        sorted_smtps = []
        for p in sorted(by_priority.keys()):
            sorted_smtps.extend(by_priority[p])
        
        # Round-robin selection
        if sorted_smtps:
            index = last_index % len(sorted_smtps)
            selected = sorted_smtps[index]
            cache.set(cache_key, index + 1, timeout=3600)  # 1 hour expiry
            
            logger.info(f"Selected SMTP {selected.host} (priority={selected.priority}, index={index}) for {email_type}")
            return selected
        
        return None
    
    @staticmethod
    def record_success(config, latency_ms=0):
        """Record successful send with latency"""
        config.sent_today += 1
        config.sent_this_hour += 1
        config.failure_count = 0
        config.health_score = min(100, config.health_score + 5)
        config.last_used_at = timezone.now()
        
        if latency_ms > 0:
            # Update rolling average for response time
            config.avg_response_time_ms = (
                (config.avg_response_time_ms * 9 + latency_ms) / 10
            )
        
        config.save()
        logger.debug(f"SMTP {config.host} success recorded (health={config.health_score})")
    
    @staticmethod
    def record_failure(config):
        """Record failed send and update health"""
        config.failure_count += 1
        config.last_failed_at = timezone.now()
        config.health_score = max(0, config.health_score - 10)
        
        if config.failure_count >= 5:
            config.is_active = False
            logger.warning(f"SMTP {config.host} auto-disabled after {config.failure_count} failures")
        
        config.save()
        logger.debug(f"SMTP {config.host} failure recorded (health={config.health_score})")
    
    @staticmethod
    def get_stats(organization):
        """Get SMTP usage statistics for the organization"""
        stats = []
        for config in organization.smtpconfig_set.all():
            stats.append({
                'host': config.host,
                'name': config.name,
                'priority': config.priority,
                'is_active': config.is_active,
                'health_score': config.health_score,
                'sent_today': config.sent_today,
                'sent_this_hour': config.sent_this_hour,
                'daily_limit': config.daily_limit,
                'hourly_limit': config.hourly_limit,
                'failure_count': config.failure_count,
            })
        return stats