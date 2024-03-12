from celery import shared_task
import datetime

from youtube.utils.internal.celery_util import SyncLatestYtVideo


@shared_task()
def sync_latest_yt_video():
    start_time = datetime.datetime.now()
    print("[sync_latest_yt_video] Started job at {}".format(start_time))
    SyncLatestYtVideo.sync_video()
    time_diff = datetime.datetime.now() - start_time
    print("[sync_latest_yt_video] Finished job at {} --> time took -->{}".format(datetime.datetime.now(),
                                                                                 time_diff))
