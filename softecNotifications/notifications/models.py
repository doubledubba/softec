from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from softecNotifications import settings

'''TODO

Make decisions on what can and should be NULL
improve aesthetics of the admin page

'''

class RestrictedHoursModel(models.Model):
    startHours = models.DateTimeField("Start hours", blank=True, null=True)
    endHours = models.DateTimeField("End hours", blank=True, null=True)

    def __unicode__(self):
        attr = 'name'
        if hasattr(self, attr):
            return getattr(self, attr)

    class Meta:
        abstract = True

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

class Restaurant(RestrictedHoursModel):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    phone = models.CharField(max_length=11, blank=True)
    refusalMsg = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True, help_text='Enable/Disable monitoring')
    alert = models.BooleanField(default=True, help_text='Enable/Disable alerts on failure')
    agents = models.ManyToManyField(Agent, blank=True)
    owners = models.ManyToManyField(Owner, blank=True)

    def title(self):
        return '%s in %s, %s' % (self.name, self.city, self.state)
        

class Computer(models.Model):
    name = models.CharField(max_length=80)
    cid = models.IntegerField(blank=True, null=True, default=0)
    
    def __unicode__ (self): return unicode(self.cid)

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
    if created:
        print instance, 'created'
        highest = settings.getHighestID() + 1
        instance.cid = highest
        settings.setHighestID(highest)
        instance.save()
        
