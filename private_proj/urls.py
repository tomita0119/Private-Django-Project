from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'private_proj.views.index'),
    url(r'^surm/', include('surm.urls')),
    url(r'^accounts/profile/', 'private_proj.views.profile'),
   
    url(r'^admin/', include(admin.site.urls)),
)
