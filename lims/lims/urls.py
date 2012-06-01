from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Team01_LIMS_site.views.home', name='home'),
    # url(r'^Team01_LIMS_site/', include('Team01_LIMS_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', include('normal_user.urls')),
    url(r'^normal-user/', include('normal_user.urls')),
    url(r'^counter-admin/', include('counter_admin.urls')),
    url(r'^book-admin/', include('book_admin.urls')),
    url(r'^user-admin/', include('user_admin.urls')),
                       
    url(r'^login/$', 'lims.views.login'),
    url(r'^loggedin/$', 'lims.views.loggedin'),
    url(r'^logout/$', 'lims.views.logout'),
    url(r'^user_passes_test/$', 'lims.views.need_normal_user_logged_in'),
)
