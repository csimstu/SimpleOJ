#@PydevCodeAnalysisIgnore
from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import problems.views
import judges.views
import accounts.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SimpleOJ.views.home', name='home'),
    # url(r'^SimpleOJ/', include('SimpleOJ.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),                              
    url(r'^show_problem/(\d+)$', problems.views.show_problem_view),         
    url(r'^problemset/$', problems.views.problemset_view),                  
    url(r'^submit/$', judges.views.submit_view),                            
    url(r'^login/$', accounts.views.login_view),                            
    url(r'^logout/$', accounts.views.logout_view),                          
    url(r'^status/$', judges.views.status_view),                            
    url(r'^userdata/(\d+)$', accounts.views.userdata_view),                 
    url(r'^update_profile/', accounts.views.update_profile_view),           
    url(r'^register/', accounts.views.registration_view),                   
    url(r'^ranklist/', accounts.views.ranklist_view),                       
    url(r'^submit/(\d*)$', judges.views.submit_view),                       
    url(r'^ckeditor/', include('ckeditor.urls')),
)
