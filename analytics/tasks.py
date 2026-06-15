import logging

from celery import shared_task
from django.utils import timezone

from organizations.models import Organization
from .services import AnalyticsService

logger = logging.getLogger(__name__)


@shared_task
def refresh_organization_analytics(organization_id):
    try:
        organization = Organization.objects.get(id=organization_id)
    except Organization.DoesNotExist:
        return {"status": "missing", "organization_id": str(organization_id)}

    AnalyticsService.refresh_organization_analytics(organization)
    return {"status": "ok", "organization_id": str(organization.id)}


@shared_task
def refresh_campaign_analytics(campaign_id):
    from campaigns.models import Campaign

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return {"status": "missing", "campaign_id": str(campaign_id)}

    AnalyticsService.refresh_campaign_analytics(campaign)
    return {"status": "ok", "campaign_id": str(campaign.id)}


@shared_task
def refresh_all_analytics():
    total_campaigns = 0
    total_links = 0
    total_orgs = 0

    for organization in Organization.objects.filter(is_active=True):
        total_campaigns += AnalyticsService.refresh_all_campaign_analytics(organization)
        total_links += AnalyticsService.refresh_link_analytics(organization)
        AnalyticsService.refresh_organization_analytics(organization)
        AnalyticsService.refresh_daily_analytics(organization)
        total_orgs += 1

    logger.info("Analytics refreshed for %s organizations.", total_orgs)

    return {
        "organizations": total_orgs,
        "campaigns_refreshed": total_campaigns,
        "link_groups_refreshed": total_links,
    }


@shared_task
def update_daily_stats():
    updated = 0

    for organization in Organization.objects.filter(is_active=True):
        AnalyticsService.refresh_daily_analytics(organization, timezone.localdate())
        AnalyticsService.refresh_organization_analytics(organization)
        updated += 1

    return {"updated": updated}


@shared_task
def refresh_link_analytics():
    count = AnalyticsService.refresh_link_analytics()
    return {"link_groups_refreshed": count}
