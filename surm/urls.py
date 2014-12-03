from django.conf.urls import patterns, include, url

urlpatterns = patterns('surm.views',
    url(r'^$', 'index'),
    url(r'^cre_group/', 'cre_group'),
    url(r'^(?P<group_id>\d+)/$', 'group_index'),
    url(r'^(?P<group_id>\d+)/add_group_member', 'add_group_member'),
    
    url(r'^accounts/', include('registration.backends.default.urls'))
)
