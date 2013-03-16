from django.db import models

class RestrictedHoursModel(models.Model):
    startHours = models.DateTimeField("Start hours")
    endHours = models.DateTimeField("End hours")

    def __unicode__(self):
        attr = 'name'
        if hasattr(self, attr):
            return getattr(self, attr)

    class Meta:
        abstract = True

class BaseContact(RestrictedHoursModel):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=11)

    def __unicode__(self):
        return self.name
        
    class Meta:
        abstract = True
        
class Agent(BaseContact):
    pass
    # figure out a many to many relationship here between
    # the agent and the restaurant models

class Owner(BaseContact):
    restaurant = models.ForeignKey('Restaurant')

class Restaurant(RestrictedHoursModel):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    refusalMsg = models.CharField(max_length=80)
    email = models.EmailField()
    notes = models.TextField()
    active = models.BooleanField()
    alert = models.BooleanField()
    # agent = models.ManyToManyField(Agent)

    def owners(self):
        string = ''
        for owner in self.owner_set.all():
            string += '%s, ' % owner.name
        if string:
            string = string[0:-2]
        return string

    owners.short_description = 'Restaurant Owners'

