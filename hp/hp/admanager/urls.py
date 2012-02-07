from django.conf.urls.defaults import patterns, include, url
from hp.admanager.views import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                      ('^admanager/$', adManager),
                      ('^createclient/$', createClient),
                      ('^createclient/success/$', createClientSuccess),
                      ('^addinternalad/$', addInternalAd),
                      ('^addinternalad/success/$', createAdSuccess),
                      ('^addexternalad/$', addExternalAd),
                      ('^addexternalad/success/$', createAdSuccess),
                      ('^deleteads/$', deleteAds),   
                      ('^deleteads/success/$', deleteAdsSuccess),    
                      ('^editinternalad/$', editInternalAd),
                      ('^editinternalad/success/$', editInternalAdSuccess),
                      #('^editexternalad/$', editExternalAd),
                      #('^editexternalad/success/$', editExternalAdSuccess),                   
)


