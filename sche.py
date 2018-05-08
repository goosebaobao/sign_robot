# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from robot import SmzdmRobot

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(filename)s] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='smzdm.log',
                    filemode='a')
scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', day='*', hour='0', minute='30', second='0')
def smzdm_sign():
    logging.info('smzdm sign...')
    smzdm = SmzdmRobot('login_id', 'password')
    smzdm.sign()

logging.info('scheduler start...')
scheduler.start()
