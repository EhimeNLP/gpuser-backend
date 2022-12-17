from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.db.utils import OperationalError
from django.utils.timezone import make_aware

from .models import FetchTime
from .views import update_gpu_status


def periodic_execution():
    try:
        update_gpu_status()
        print("periodic execution")
    except OperationalError:
        print("periodic execution failed")


def remove_old_data():
    # remove data older than 1 day
    now_aware = make_aware(datetime.now())
    FetchTime.objects.filter(fetch_time__lt=now_aware - timedelta(days=1)).delete()
    print("remove old data")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        periodic_execution,
        "interval",
        seconds=10,
        max_instances=1,
        misfire_grace_time=1,
    )
    scheduler.add_job(
        remove_old_data, "interval", hours=1, max_instances=1, misfire_grace_time=1
    )
    scheduler.start()
