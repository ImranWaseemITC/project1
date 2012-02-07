from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$','hp.views.homepage'),
                       url('', include('medicalcontent.urls')),
                       url('', include('user.urls')),
                       url('', include('groupmanager.urls')),
                       url('', include('forum.urls')),
                       url('', include('admanager.urls')),
					   url('', include('patienthealthrecord.urls')),
                       url('', include('news.urls')),
                       url('', include('phr.urls')),
                       
                       #(r'^ckeditor/', include('ckeditor.urls')),
                       (r'^aboutus/', 'hp.views.aboutus'),
                       (r'^send_feedback/', 'hp.views.send_email'),
                       (r'^refresh_page/', 'hp.views.refreshpage'),
                       
    # Examples:
    # url(r'^$', 'hp.views.home', name='home'),
    # url(r'^hp/', include('hp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )