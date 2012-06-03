from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('normal_user.views',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),
    #url(r'^test/$', 'normal_user.views.login'),
    url(r'^information/$', 'information'),
    url(r'^allbook/$', 'allbook'),
    url(r'^borrow/$', 'borrowbook'),
    url(r'^renewal/$', 'renewal'),
    url(r'^base/$', 'base'),
    url(r'^test/$', 'test'),
    url(r'^$', 'test'),
)
