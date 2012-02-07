from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^login/$','user.views.login'),
                       (r'^logout/$','user.views.logout'),
                       (r'^signup/$','user.views.signup'),
    # Examples:
    # url(r'^$', 'HP.views.home', name='home'),
    # url(r'^HP/', include('HP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)