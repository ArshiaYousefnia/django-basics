import random
import time

from testdjangoProject.celery_config import app
from celery.schedules import crontab

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from celery import signals


@signals.celeryd_init.connect
def init_sentry(**kwargs):
    sentry_sdk.init(
        dsn="https://0a9e769ee4b62da3bda274bbbccf5f92@sentry.sabz.dev/663",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[CeleryIntegration(monitor_beat_tasks=True)],
        environment="local.dev.grace",
        release="v1.0",
    )


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), dummy_task.s(), name='dummy_task')
    sender.add_periodic_task(crontab(minute='*/1'), dummy_task2.s(), name='dummy_task2')
    sender.add_periodic_task(crontab(minute="*/1"), dummy_task3.s(), name='dummy_task3')


@app.task(name='dummy_task')
def dummy_task():
    i = random.randint(10, 150)
    j = 0
    for i in range(100):
        j += i
        time.sleep(0.5)

    print(i, ":", j, sep="")


@app.task(name='dummy_task2')
def dummy_task2():
    time.sleep(50)
    print("done")


@app.task(name='dummy_task3')
def dummy_task3():
    time.sleep(1)
    print("done done")
