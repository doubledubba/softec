from datetime import datetime, time
import json

from django.utils.timezone import utc
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from softecNotifications import settings, choices
from notifications.helpers import logging

'''TODO

Make decisions on what can and should be NULL
improve aesthetics of the admin page

'''

logger = logging.getLogger(__name__)

class RestrictedHoursModel(models.Model):
    startHours = models.TimeField("Start hours", blank=True, null=True)
    endHours = models.TimeField("End hours", blank=True, null=True)

    def __unicode__(self):
        attr = 'name'
        if hasattr(self, attr):
            return getattr(self, attr)

    class Meta:
        abstract = True

    def available(self):
        if self.endHours == time(hour=0, minute=0):
            self.endHours = time(hour=23, minute=59, second=59)
        # what if there are no defined hours?
        if not self.startHours or not self.endHours:
            return True
        return self.startHours < datetime.now().time() < self.endHours

class BaseContact(RestrictedHoursModel):
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=11, blank=True)

    def __unicode__(self):
        return self.name
        
    class Meta:
        abstract = True
        
class Agent(BaseContact):
    pass

class Owner(BaseContact):
    def restaurants(self):
        querySet = self.restaurant_set.all()
        return querySetToStr(querySet, 'title')
    restaurants.short_description = 'Owned restaurants'


class Computer(models.Model):
    name = models.CharField(max_length=80)
    cid = models.IntegerField(blank=True, null=True, default=0, unique=True) # shouldn't be visible in admin page
    restaurant = models.ForeignKey('Restaurant')
    os = models.CharField("Operating system", max_length=100, choices=choices.os, blank=True)
    pos = models.CharField(max_length=100, choices=choices.pos, blank=True)
    description = models.TextField(max_length=255, blank=True)
    online = models.BooleanField(default=False)
    active = models.BooleanField('Active?', default=True)

    failures = models.TextField(blank=True)
    last_check_in = models.DateTimeField(null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    first_check_in = models.BooleanField('First check in?', default=True)
    notify_on_fail = models.BooleanField(default=True)
    js_warning = models.BooleanField(default=True)

    @staticmethod
    def get_actives():
        'Query all active computers'
        return Computer.objects.filter(restaurant__active=True, active=True)
    
    def __unicode__ (self):
        return unicode(self.cid)

    def get_absolute_url(self):
        return '/computer/%d' % self.cid

    def is_active(self):
        'Active if restaurant and computer are active'

        return self.restaurant.active and self.active


    def check_in(self):
        'Clean method of checking in computers periodically. As simple as calling.'

        if not self.is_active():
            response = '%d failed to check in because it is not active' % self.cid
            logger.debug(response)
            return response
        else:
            self.last_check_in = datetime.utcnow().replace(tzinfo=utc)
            self.online = True
            self.save()
            response = "CID=%d checked in on %s" % (self.cid, datetime.now().strftime('%c'))
            logger.info(response)
            return response

    def stamp_update(self):
        '''Use to show which computers have been updated with most recent
        CHECK_IN_RATE. Just call it when they are updated.'''

        self.last_update = datetime.utcnow().replace(tzinfo=utc)
        self.save()

    def getLatency(self):
        """Returns the latency of a Computer expressed in seconds (int)."""

        now = datetime.utcnow().replace(tzinfo=utc)
        latency = (now - self.last_check_in).seconds
        return latency

    def get_badge(self):
        """Used for rendering the correct badge on the /listings page.

        Put the code into a method to remove logic on the template side"""

        if not self.is_active():
            return 'badge badge-inverse'
        elif self.online:
            return 'badge badge-success'
        elif self.first_check_in:
            return 'badge'
        elif self.restaurant.available():
            return 'badge badge-warning'
        else:
            return 'badge badge-important'

    def to_dict(self, wRestaurant=False):
        """Converts Model instance into a serializable dictionary for JSON conversion.

        If wRestaurant=True, the restaurant object will be included as it's own dictionary."""
        jComputer = {
            'name': self.name,
            'cid': self.cid,
            'is_active': self.is_active(),
            'online': self.online,
            'notify_on_fail': self.notify_on_fail,
            'js_warning': self.js_warning,
            'get_badge': self.get_badge(),
            'url': self.get_absolute_url(),
        }
        if wRestaurant:
            jComputer['restaurant'] = self.restaurant.to_dict(wComputers=False)
        return jComputer


class Restaurant(RestrictedHoursModel):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80, choices=choices.states)
    phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True, null=True)
    refusalMsg = models.CharField(max_length=80, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True, help_text='Enable/Disable monitoring')
    agents = models.ManyToManyField(Agent, blank=True)
    owners = models.ManyToManyField(Owner, blank=True)

    def get_absolute_url(self):
        return '/restaurant/%d' % self.pk

    def title(self):
        return '%s in %s, %s' % (self.name, self.city, self.state)

    def to_dict(self, wComputers=False):
        """Converts Model instance into a serializable dictionary for JSON conversion.

        If wComputer=True, the computer objects will be included as a list of dicts."""
        jRestaurant = {
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'url': self.get_absolute_url(),
            'active': self.active,
        }
        if wComputers:
            jRestaurant['computers'] = []
            for computer in self.computer_set.all():
                computer_dict = computer.to_dict(wRestaurant=False)
                jRestaurant['computers'].append(computer_dict)
        return jRestaurant


def querySetToStr(objects, attr):
    '''Turns a list of ORM instances into a nice string.

    Pass in a list of ORM instances
    pass in a str attribute or a str returning callable of the instances in that set'''

    string = ''
    for obj in objects:
        attribute = getattr(obj, attr)
        if callable(attribute):
            mod = attribute()
        else:
            mod = attribute
        string += '%s, ' % mod
    if string:
        string = string[0:-2]
        
    return string
    
    
@receiver(post_save, sender=Computer)
def init_cid(sender,instance, signal, created, **kwargs):
    'Makes sure that each cid is unique on Computer instance creation'
    if created:
        highest = settings.getHighestID() + 1
        instance.cid = highest
        settings.setHighestID(highest)
        instance.save()
        
