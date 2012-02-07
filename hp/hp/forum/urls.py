from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^forum/([a-z0-9=\?\&]*)/?$','forum.views.displayTopic'),
                       url(r'^forum/(?P<view_all>[\w\-]{1,8})/?$','forum.views.displayAllThreads'),
                       url(r'^orderby/(datedtime)/?$','forum.views.orderForumActivityHome'),
                       url(r'^orderby/(mostpopular)/?$','forum.views.orderForumActivityHome'),
                       url(r'^orderby/(mostdiscuss)/?$','forum.views.orderForumActivityHome'),
                       url(r'^orderbyforum/([a-z0-9=\?\&]*)/?$','forum.views.orderMoreForumActivity'),
                       url(r'^see_more/([a-z0-9=\?\&]*)/?$','forum.views.orderMoreForumActivity'),
                       url(r'^topic/([A-Z a-z 0-9 \-]+)/?$','forum.views.forumContentByTopic'),
                       
                       url(r'^searchthread/?(?P<is_adv>adv)?/?$','forum.views.search'),
                       
                       url(r'^upvote/(?P<thread_id>[\w\d\-]{1,36})/(?P<topic_id>[\w\d\-]{1,36})?/?(?P<origthread_id>[\w\d\-]{1,36})?/?(?P<view_all>[\w\d\-]{1,36})?/?$','forum.views.threadVote',{'up':True}),
                       url(r'^downvote/(?P<thread_id>[\w\d\-]{1,36})/(?P<topic_id>[\w\d\-]{1,36})?/?(?P<origthread_id>[\w\d\-]{1,36})?/?(?P<view_all>[\w\d\-]{1,36})?/?$','forum.views.threadVote',{'down':True}),

                       url(r'''^locktopic/(?P<object_id>[\w\d\-]{1,36})/(?P<disptopic_id>[\w\d\-]{1,36})?/?(?P<return_to_forum>True)?/?$''',
                           'forum.views.locker',
                           {'lock':True, 'object_type':'topic'}),
                       url(r'''^unlocktopic/(?P<object_id>[\w\d\-]{1,36})/(?P<disptopic_id>[\w\d\-]{1,36})?/?(?P<return_to_forum>True)?/?$''',
                           'forum.views.locker',
                           {'lock':False, 'object_type':'topic'}),
                       url(r'''^lockthread/(?P<object_id>[\w\d\-]{1,36})/(?P<disptopic_id>[\w\d\-]{1,36})?/?(?P<return_to_forum>True)?/?$''',
                           'forum.views.locker',
                           {'lock':True, 'object_type':'thread'}),
                       url(r'''^unlockthread/(?P<object_id>[\w\d\-]{1,36})/(?P<disptopic_id>[\w\d\-]{1,36})?/?(?P<return_to_forum>True)?/?$''',
                           'forum.views.locker',
                           {'lock':False, 'object_type':'thread'}),
                       
                       url(r'^forum/newthread/(?P<topic_id>[\w\d\-]{1,36})/(?P<parent_id>[\w\d\-]{1,36})/(?P<origthread_id>[\w\d\-]{1,36})/?$','forum.views.newThread'),
                       url(r'^forum/newthread/(?P<topic_id>[\w\d\-]{1,36})/?$','forum.views.newThread', {'is_parent':True}),
            
                       url(r'^read_news/(?P<news_id>[\w\d\-]{1,36})/newthread/(?P<topic_id>[\w\d\-]{1,36})/(?P<parent_id>[\w\d\-]{1,36})/(?P<origthread_id>[\w\d\-]{1,36})/?$','forum.views.newThread'),
                       
                       #url(r'^forum/newthread/?$','forum.views.newThread', {'is_parent':True}),
                       url(r'^forum/editthread/(?P<thread_id>[\w\d\-]{1,36})/(?P<view_page>[\w\d\-]{1,36})/(?P<topic_id>[\w\d\-]{1,36})/?(?P<parent_id>[\w\d\-]{1,36})?/?$','forum.views.editThread'),
                       url(r'^threadreply/(?P<topic_id>[\w\d\-]{1,36})/(?P<parent_id>[\w\d\-]{1,36})/?$','forum.views.displayTopic'),
                       
                       url(r'^forum/editcategory/(?P<category_id>[\w\d\-]{1,36})/?(?P<topic_id>[\w\d\-]{1,36})?/?(?P<thread_id>[\w\d\-]{1,36})?/?$','forum.views.editCategory'),
                       url(r'^forum/deletecategory/(?P<category_id>[\w\d\-]{1,36})/?(?P<topic_id>[\w\d\-]{1,36})?/?(?P<thread_id>[\w\d\-]{1,36})?/?$','forum.views.deleteCategory'),
                       url(r'^forum/deletethread/(?P<thread_id>[\w\d\-]{1,36})/(?P<view_page>[\w\d\-]{1,36})/?(?P<topic_id>[\w\d\-]{1,36})?/?(?P<parent_id>[\w\d\-]{1,36})?/?$','forum.views.deleteThread'),
    # url(r'^$', 'HP.views.home', name='home'),
    # url(r'^HP/', include('HP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
