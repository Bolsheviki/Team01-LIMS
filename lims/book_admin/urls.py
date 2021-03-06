from django.conf.urls import patterns, include, url
#from django.views.generic.simple import direct_to_template
#from lims import util

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()



urlpatterns = patterns('book_admin.views',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),

#    url(r'^$', direct_to_template, { 'template': 'book_admin/index.html', 'extra_context': {'app' : 'book-admin', 'books': util.get_top3_books_in_month() }, }),

    url(r'^$', 'index'),
	url(r'^login/$', 'login'),
	url(r'^logout/$', 'logout'),
	url(r'^settings/$', 'settings'),

    url(r'^search/$', 'search'),
    url(r'^add/$', 'add'),
    url(r'^remove/$', 'remove'),
    url(r'^audit/$', 'audit'),
    url(r'^book/(?P<isbn>\d+)/$', 'info_book'),
)
