from django.conf.urls import patterns, include, url

urlpatterns = patterns('surm.views',
    url(r'^$', 'index'),
    url(r'^cre_group/', 'cre_group'),
    url(r'^(?P<group_id>\d+)/$', 'group_index'),
    url(r'^(?P<group_id>\d+)/add_group_member', 'add_group_member'),
    url(r'^(?P<group_id>\d+)/settings', 'group_settings'),
    url(r'^(?P<group_id>\d+)/(?P<tag_id>\d+)/$', 'tag_filtering'),
    url(r'^(?P<group_id>\d+)/favorite', 'my_favorite'),
    url(r'^(?P<group_id>\d+)/get_resourcetitle_error', 'get_resourcetitle_error'),
    
    url(r'^accounts/', include('registration.backends.default.urls')),
)
