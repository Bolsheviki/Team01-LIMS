from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('normal_user.views',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),
    
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^search/$', 'search'),
    url(r'^settings/$', 'settings'),
    url(r'^information/$', 'information'),
#    url(r'^allbook/$', 'allbook'),
#    url(r'^borrow/$', 'borrowbook'),
    url(r'^renewal/$', 'renewal'),
    url(r'^book/(?P<isbn>\d+)/$', 'info_book'),
    url(r'^$', 'search'),
)
