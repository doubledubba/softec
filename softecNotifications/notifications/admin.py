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
