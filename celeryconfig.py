from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'compute-and-store-faqs-every-two-weeks': {
        'task': 'tasks.compute_and_store_faqs',
        'schedule': crontab(day_of_week='mon', hour='0', minute='0'),
    },
}

CELERY_TIMEZONE = 'UTC'
