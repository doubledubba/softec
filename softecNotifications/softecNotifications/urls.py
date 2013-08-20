from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index'),
    url(r'^logout/$', 'home.views.logout_user'),
    url(r'^login/$', 'home.views.login_user'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('notifications.views',
    url(r'^update/$', 'update_view'),
    url(r'check_in/$', 'check_in_view'),
    url(r'^listings/$', 'listings'),
    url(r'^listings/json$', 'listings_json'),
)
