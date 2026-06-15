import os

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# =========================
# QUEUES
# =========================
app.conf.task_queues = [
    Queue("high_priority", Exchange("high_priority"), routing_key="high_priority"),
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("low_priority", Exchange("low_priority"), routing_key="low_priority"),
]

app.conf.task_default_queue = "default"
app.conf.task_default_exchange = "default"
app.conf.task_default_routing_key = "default"

# =========================
# ROUTING
# =========================
app.conf.task_routes = {
    # Email engine
    "email_engine.tasks.process_high_priority_email": {
        "queue": "high_priority",
        "routing_key": "high_priority",
    },
    "email_engine.tasks.process_email_job": {
        "queue": "default",
        "routing_key": "default",
    },
    "email_engine.tasks.process_due_email_jobs": {
        "queue": "default",
        "routing_key": "default",
    },
    "email_engine.tasks.retry_failed_jobs": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "email_engine.tasks.reset_smtp_minute_counters": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "email_engine.tasks.reset_smtp_hourly_counters": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "email_engine.tasks.reset_smtp_daily_counters": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "email_engine.tasks.check_smtp_health": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "email_engine.tasks.cleanup_old_email_jobs": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "email_engine.tasks.cleanup_old_email_jobs_including_failed": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },

    # Other apps
    "analytics.tasks.update_campaign_stats": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "analytics.tasks.update_daily_stats": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "webhooks.tasks.deliver_webhook": {
        "queue": "default",
        "routing_key": "default",
    },
    "webhooks.tasks.retry_failed_webhooks": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
    "notifications.tasks.send_daily_digest": {
        "queue": "low_priority",
        "routing_key": "low_priority",
    },
}

# =========================
# WORKER BEHAVIOR
# =========================
app.conf.task_time_limit = 30 * 60
app.conf.task_soft_time_limit = 25 * 60

app.conf.task_track_started = True
app.conf.task_send_sent_event = True

app.conf.result_expires = 86400

app.conf.worker_prefetch_multiplier = 4
app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True

# =========================
# BEAT SCHEDULE
# =========================
app.conf.beat_schedule = {
    'process-pending-campaigns': {
        'task': 'campaigns.tasks.process_pending_campaigns',
        'schedule': crontab(minute='*/1'),
        'options': {'queue': 'default'},
    },
    "process-due-email-jobs-every-minute": {
        "task": "email_engine.tasks.process_due_email_jobs",
        "schedule": crontab(minute="*"),
        "options": {"queue": "default"},
    },
    "reset-smtp-minute-counters": {
        "task": "email_engine.tasks.reset_smtp_minute_counters",
        "schedule": crontab(minute="*"),
        "options": {"queue": "low_priority"},
    },
    "reset-smtp-hourly-counters": {
        "task": "email_engine.tasks.reset_smtp_hourly_counters",
        "schedule": crontab(minute=0),
        "options": {"queue": "low_priority"},
    },
    "reset-smtp-daily-counters": {
        "task": "email_engine.tasks.reset_smtp_daily_counters",
        "schedule": crontab(minute=0, hour=0),
        "options": {"queue": "low_priority"},
    },
    "check-smtp-health": {
        "task": "email_engine.tasks.check_smtp_health",
        "schedule": crontab(minute="*/15"),
        "options": {"queue": "low_priority"},
    },
    "retry-failed-email-jobs": {
        "task": "email_engine.tasks.retry_failed_jobs",
        "schedule": crontab(minute="*/10"),
        "options": {"queue": "low_priority"},
    },
    "cleanup-old-email-jobs": {
        "task": "email_engine.tasks.cleanup_old_email_jobs",
        "schedule": crontab(hour=2, minute=0),
        "options": {"queue": "low_priority"},
    },

    "update-analytics": {
        "task": "analytics.tasks.update_daily_stats",
        "schedule": crontab(hour=1, minute=0),
        "options": {"queue": "low_priority"},
    },
    "retry-failed-webhooks": {
        "task": "webhooks.tasks.retry_failed_webhooks",
        "schedule": crontab(minute="*/10"),
        "options": {"queue": "low_priority"},
    },
    "send-daily-digest": {
        "task": "notifications.tasks.send_daily_digest",
        "schedule": crontab(hour=9, minute=0),
        "options": {"queue": "low_priority"},
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
