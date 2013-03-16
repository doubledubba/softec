from django.db import models

class RestrictedHoursModel(models.Model):
    startHours = models.DateTimeField("Start hours")
    endHours = models.DateTimeField("End hours")
    
    class Meta:
        abstract = True

class BaseContact(RestrictedHoursModel):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
        
    class Meta:
        abstract = True
        
class Agent(BaseContact):
    pass

class Owner(BaseContact):
    restaurant = models.ForeignKey('Restaurant')

    def __unicode__(self):
        return self.name

class Restaurant(RestrictedHoursModel):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name

    def owners(self):
        string = ''
        for owner in self.owner_set.all():
            string += '%s, ' % owner.name
        if string:
            string = string[0:-2]
        return string

