from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AAapp.views.home', name='home'),
    # url(r'^AAapp/', include('AAapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'AAapp.AA.views.welcome'),
    url(r'^accounts/login/$', 'AAapp.AA.views.welcome'),
    url(r'^new_expense/$', 'AAapp.AA.views.new_expense'),
    url(r'^view_expense/(\d+)/', 'AAapp.AA.views.view_expense'),
    url(r'^logout/$', 'AAapp.AA.views.signoff'),
    url(r'^new_account/$', 'AAapp.AA.views.new_account'),
)

