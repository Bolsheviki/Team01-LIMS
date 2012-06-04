from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('user_admin.views',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),
    url(r'^$', 'search'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^search$', 'search'),
    url(r'^settings$', 'settings'),
    url(r'^add/$', 'add'),
    url(r'^remove/$', 'remove'),
    url(r'^user/(?P<username>\w+)/$', 'info_user'),
)