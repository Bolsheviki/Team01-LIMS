from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('book_admin.views',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),

    url(r'^$', 'search'),
    url(r'^search/$', 'search'),
    url(r'^search/(?P<page>page=\d+)/$', 'search'),
    url(r'^add/$', 'add'),
    url(r'^audit/$', 'audit'),
    url(r'^remove/$', 'audit'),
)
