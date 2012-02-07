from django.conf.urls.defaults import patterns, include, url
from hp.phr.views import *
from django.conf import settings

urlpatterns = patterns('',
                      ('^phrprofiles$', displayProfiles),
                      ('^phrprofile$', addProfile),
                                               
)


