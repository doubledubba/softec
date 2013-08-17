from django.contrib import admin
from notifications.models import Agent, Owner, Restaurant, Computer

class ContactAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Hours of Operation', {
            'fields': ('startHours', 'endHours')
        }),
    )

class AgentAdmin(ContactAdmin):
    list_display = ('name', 'email', 'phone')

class OwnerAdmin(ContactAdmin):
    '''Should show the owner's corresponding restaurant'''
    list_display = ('name', 'email', 'phone', 'restaurants')
    list_editable = ('email', 'phone')


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Agent, AgentAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Computer)

