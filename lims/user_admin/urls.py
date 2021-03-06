from django.conf.urls import patterns, include, url
#from django.views.generic.simple import direct_to_template
#from lims import util

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('user_admin.views',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),
#    url(r'^$', direct_to_template, { 'template': 'user_admin/index.html', 'extra_context': {'app' : 'user-admin', 'books': util.get_top3_books_in_month() }, }),

    url(r'^$', 'index'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^search$', 'search'),
    url(r'^settings$', 'settings'),
    url(r'^add/$', 'add'),
    url(r'^add-one/$', 'add_one'),
    url(r'^remove/$', 'remove'),
    url(r'^user/(?P<username>\w+)/$', 'info_user'),
    url(r'^rm-user/(?P<username>\w+)/$', 'rm_user'),
)
