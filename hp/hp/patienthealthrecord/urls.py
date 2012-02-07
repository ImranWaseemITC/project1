from django.conf.urls.defaults import patterns, include, url
from hp.patienthealthrecord.views import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                      ('^createpatienthealthrecord/$', createPatientHealthRecord),
                      ('^createpatienthealthrecord/success/$', createPatientHealthRecordSuccess),
                      ('^managepatienthealthrecord/$', managePatientHealthRecord),
                      ('^deletepatienthealthrecord/success/$', deletePatientHealthRecordSuccess),)

