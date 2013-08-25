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
    url(r'^listings/json/all$', 'listings_json'),
    url(r'^listings/json/offline$', 'listings_json_offline'),
    url(r'^listings/ajax$', 'ajax_listings'),
)
'''
urlpatterns += patterns('knowledge.views',

    url(r'^knowledge/$', 'index'),
    url(r'^knowledge/(?P<pk>.+)/$', 'show_article'),
    url(r'^knowledge/(?P<pk>.+)/raw$', 'show_raw_article'),
    )'''
