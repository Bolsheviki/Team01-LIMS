from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

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
<<<<<<< HEAD
    url(r'^$', direct_to_template,{'template': 'normal_user/index.html',}),
=======
    url(r'^$', direct_to_template, { 'template': 'normal_user/index.html', 'extra_context': {'app' : 'normal-user'}, }),
>>>>>>> b01c89cc9d57e542d156c796952a9e0267b028f5
)
