from django.contrib import admin
from notifications.models import Agent, Owner, Restaurant


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')

class OwnerAdmin(admin.ModelAdmin):
    '''Should show the owner's corresponding restaurant'''
    list_display = ('name', 'restaurant', 'email', 'phone')

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owners',)

admin.site.register(Agent, AgentAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Restaurant, RestaurantAdmin)

'''

    name - charField
    address - charField
    city - charField
    state - charField (choice)
    email - charField
    notes - textField
    active - booleanField (reject tracking if false)
    alert - booleanField [track if active, but (do || not)alert ]
    agent - ForeignKey TODO: More than one? Many to Many
    refusalMsg - charField
'''
