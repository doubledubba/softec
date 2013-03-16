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
        
    def __unicode__(self):
        return self.name
        
class Agent(BaseContact):
    pass
    
class Owner(BaseContact):
    pass
    
