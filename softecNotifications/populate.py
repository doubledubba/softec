import os
from datetime import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'softecNotifications.settings'

from notifications.models import Restaurant, Agent, Owner



gabriel_info = {
        'name': 'Gabriel',
        'email': 'gabriel@softecpos.com',
        'phone': '14259714407',
        'startHours': datetime.now(),
        'endHours': datetime.now()}

gabriel = Agent(**gabriel_info)
gabriel.save()

mario_info = gabriel_info
mario_info['name'] = 'Mario'
mario_info['email'] = 'mario@mazatlan.com'

mario = Owner(**mario_info)
mario.save()

restaurants = {
        'name': 'La Tapatia',
        'address': '1424 NW 194th st',
        'city': 'Seattle',
        'state': 'WA',
        'refusalMsg': '',
        'email': 'luisnaranjo733@gmail.com',
        'notes': None,
        'startHours': datetime.now(),
        'endHours': datetime.now()
        }

tapatia = Restaurant(**restaurants)
tapatia.save()
