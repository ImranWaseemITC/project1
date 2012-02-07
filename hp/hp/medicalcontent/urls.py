from django.conf.urls.defaults import patterns, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^adamcontent/(\d{1,3})/(\d{4,6})/$','hp.medicalcontent.views.getArticleContentByProductIDArticleID'),
                       url(r'^content/([A-Z]{1}[a-z]{0,1})/$','hp.medicalcontent.views.content'),
                       url(r'^search/$','hp.medicalcontent.search.search'),
                       url(r'^searchByCategory/$','hp.medicalcontent.search.searchByCategory'),
                       url(r'^content/$','hp.medicalcontent.views.displaycenters'),                       
                       url(r'^searchBySubcontent/$','hp.medicalcontent.search.searchBySubcontent'),
                       url(r'^searchByCenter/$','hp.medicalcontent.search.searchByCenter'),
                       url(r'^video/$','hp.medicalcontent.views.video'),
                       url(r'^allvideo/$','hp.medicalcontent.views.allvideo'),
                       url(r'^Encyclopedia/Conditions A-Z/$','hp.medicalcontent.conditions.conditions'),
                       url(r'^Encyclopedia/Conditions A-Z/([A-Za-z]*)/([A-Z]{1}[a-z]{0,1})/$','hp.medicalcontent.conditions.browse_condition'),
                       
    # Examples:
    # url(r'^$', 'hp.views.home', name='home'),
    # url(r'^hp/', include('hp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.static',
                        (r'^media/(?P<path>.*)$', 'serve',
                         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),        
)

urlpatterns += patterns('django.views.static',
                        (r'^xml/(?P<path>.*)$', 'serve',
                         {'document_root': settings.XML_ROOT, 'show_indexes': True}),        
)