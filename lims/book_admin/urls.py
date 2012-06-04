from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()



urlpatterns = patterns('book_admin.views',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),

    url(r'^$', 'search'),
<<<<<<< HEAD
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
=======
	url(r'^login/$', 'login'),
	url(r'^logout/$', 'logout'),
	url(r'^settings/$', 'settings'),
>>>>>>> f323b46a433391f59b02e221149f9b556789282d
    url(r'^search/$', 'search'),
    url(r'^add/$', 'add'),
    url(r'^remove/$', 'remove'),
    url(r'^audit/$', 'audit'),
    url(r'^book/(?P<isbn>\d+)/$', 'info_book'),
)
