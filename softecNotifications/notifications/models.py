from django.db import models

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
    # figure out a many to many relationship here between
    # the agent and the restaurant models

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
    refusalMsg = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    alert = models.BooleanField(default=True)
    agents = models.ManyToManyField(Agent, blank=True)
    owners = models.ManyToManyField(Owner, blank=True)

    def title(self):
        map = (self.name, self.city, self.state)
        return '%s in %s, %s' % map

def querySetToStr(objects, attr):
    '''Turns a list of ORM instances into a nice string.

    Pass in a list of ORM instances
    pass in a str attribute or a str returning callable of the instances in that set'''

    string = ''
    for object in objects:
        attribute = getattr(object, attr)
        if callable(attribute):
            mod = attribute()
        else:
            mod = attribute
        string += '%s, ' % mod
    if string:
        string = string[0:-2]
    return string
