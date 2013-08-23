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

def alert(log, message, **kwargs):
    log(message)
    print(kwargs)

logger = logging.getLogger('monitor')
logger.setLevel(logging.DEBUG)

def iterate_over_computers(computers):
    for computer in computers:

        if not computer.is_active():
            logger.debug('Skipped: %s' % computer)
            continue

        if not computer.last_check_in:
            logger.debug('%s is active but has not checked in yet' % computer)
            continue # it needs to check in first

        if computer.first_check_in and computer.last_check_in:
            logger.debug('%s has done its first check in' % computer)
            alert(logger.info, '%s has done it\'s first check in' % computer)
            computer.first_check_in = False
            computer.save()

        latency = computer.getLatency()  # int

        #print computer
        #print 'Latency:', latency
        #print 'In time:', latency < MAX_LATENCY
        #print 'Out of time:', latency > MAX_LATENCY
        #print 'Offline trigger:', latency > MAX_LATENCY and computer.notify 
        #print 'Online trigger', latency < MAX_LATENCY and not computer.notify,

        if latency > MAX_LATENCY and computer.notify_on_fail: # offline trigger
            message = "%s has not connected in %d seconds." % (computer,
                    latency)
            alert(logger.warning, message, important=True, computer=computer)
            computer.notify_on_fail = False
            computer.online = False
            failure = datetime.now().strftime('%c') + ','
            computer.save()

        if latency < MAX_LATENCY and not computer.notify_on_fail: # online trigger
            computer.notify_on_fail = True
            computer.save()
            alert(logger.info, '%s is back online.' % computer)

        if latency > MAX_LATENCY and not computer.notify_on_fail and not computer.first_check_in and computer.online:
            computer.notify = True
            computer.save()
            alert(logger.warning, 'Saved %s from limbo' % computer)
            #iterate_over_computers(computers)
            #break
            message = "%s has not connected in %d seconds." % (computer, latency)
            alert(logger.warning, message, important=True, computer=computer)
            computer.notify_on_fail = False
            computer.online = False
            failure = datetime.now().strftime('%c') + ','
            computer.save()


def getComputers():
    for computer in Computer.objects.all():
        if computer.is_active():
            yield computer
        else:
            print computer, 'is not being monitored.'


if __name__ == '__main__':
    iterate_over_computers(getComputers())