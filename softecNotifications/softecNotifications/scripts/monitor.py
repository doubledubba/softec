#!/usr/bin/env python2.7

import os
import sys
from datetime import datetime
import logging
sys.path.append('/home/luis/Dropbox/projects/softec/softecNotifications/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'softecNotifications.settings'
from django.utils.timezone import utc
from notifications.models import Computer

MAX_LATENCY = 45
MAX_LATENCY = 15

logger = logging.getLogger('monitor')
logger.setLevel(logging.DEBUG)

def alert(log, message, computer=None):
    log(message)
    if computer: # computer is down, now alert
        print computer

def flag(computer, notify=False):
    computer.online = False
    computer.log_action(offline=True)
    if notify:
        computer.notify_on_fail = False
    computer.save()

def flag_offline(computer):
    log = computer.get_log()
    if log:
        now = datetime.utcnow().replace(tzinfo=utc)
        most_recent = log[-1]['timeStamp']
        latency = (now - most_recent).seconds
        print 'latency: ', latency
        if latency < 180: # 3minutes
            flag(computer)
        else:
            flag(computer, True)
    else:
        flag(computer)

def iterate_over_computers(computers=None):
    computers = computers or Computer.get_actives()
    for computer in computers:
        if not computer.last_check_in:
            logger.debug('%s is active but has not checked in yet' % computer)
            continue # it needs to check in first

        if computer.first_check_in and computer.last_check_in:
            alert(logger.info, '%s has done it\'s first check in' % computer)
            computer.first_check_in = False
            computer.save()

        latency = computer.getLatency()  # int

        if latency > MAX_LATENCY and computer.notify_on_fail: # offline trigger
            message = "%s has not connected in %d seconds." % (computer,
                    latency)
            alert(logger.warning, message, computer)
            flag_offline(computer)

        if latency < MAX_LATENCY and not computer.notify_on_fail: # online trigger
            computer.notify_on_fail = True
            computer.save()
            alert(logger.info, '%s is back online.' % computer)

        if latency > MAX_LATENCY and not computer.notify_on_fail and not computer.first_check_in and computer.online: #weird limbo logic exception
            alert(logger.warning, 'Saved %s from limbo' % computer)
            message = "%s has not connected in %d seconds." % (computer, latency)
            alert(logger.warning, message, computer)
            flag_offline(computer)


if __name__ == '__main__':
    iterate_over_computers()