from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('counter_admin.views',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),
    url(r'^$', direct_to_template,{'template': 'counter_admin/index.html',}),
	url(r'^borrow/$', 'borrow'),
	url(r'^return/$', 'return_'),
	url(r'^clear/$', 'clear'),
	url(r'^login/$', 'login'),
	url(r'^logout/$', 'logout'),
	url(r'^settings$', 'settings'),
)
