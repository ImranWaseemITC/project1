from django.conf.urls.defaults import patterns, include, url
from hp.groupmanager.views import *
from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
                       ('^groupmanager/$', groupManager),
                       ('^creategroup/$', createGroup),
                       ('^deletegroup/$', deleteGroup),
                       ('^creategroup/success/$', success),
                       ('^deletegroup/success/$', deleteGroupSuccess),
                       ('^addusers/$', addUsersToGroup),
                       ('^addusers/success/$', addUsersSuccess),
                     
                       
                                               
)


