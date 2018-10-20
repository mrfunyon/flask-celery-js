import random
from time import sleep
from app import create_celery_app
from flask import g
from celery.utils.log import get_task_logger
from celery.signals import after_setup_logger
import logging
import sys

celery = create_celery_app()

logger = get_task_logger(__name__)

@celery.task()
def test_task():
    sleep(random.randint(1,5))
    return random.randint(1,100)

# @celery.task()
# def send_to_service(data):
#     from time.sleep
#     sleep()



# def test_celery_send():
#     from pathlib import Path
#     import os
#     parent = Path(__file__).resolve().parent
#     print(parent)
#     with open(os.path.join(parent, "ng_example.xml"), "r") as fp:
#         data = fp.read()

#     return send_ng_item.delay(data, 'local')
