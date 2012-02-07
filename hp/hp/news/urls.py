from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^news_feed/?$','news.views.display_feeds'),
                       url(r'^read_news/(?P<news_id>[\w\d\-]{1,36})/?$','news.views.display_feeds'),
                       )