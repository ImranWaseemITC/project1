import uuidfield
from django.db import models
from hp.user.models import user as user
from hp.groupmanager.models import group as group

class content(models.Model):
    """
    ##########################################################
    # The Content class defines a generic content object.    #
    # It has a many-to-many relationship with groups,        #
    # and also a many-to-many relationship with User which   #
    # has been defined to cater for quick access to users    #
    # that are assigned rights to a particular content.      #
    # The Content class also has a foreign key field of      #
    # User type that defines the owner/creator of the content#
    ##########################################################
    """
    id = uuidfield.UUIDField(auto=True, editable=False, primary_key=True)
    contentAlias = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    contentBody = models.TextField()
    contentDate = models.DateTimeField()
    #User = models.ManyToManyField(user, through='content_user')
    #Group = models.ManyToManyField(group, through='content_group') 
    ownerUser = models.ForeignKey(user, related_name = 'ownsContent')
    
    def __str__(self):
        return "%s" %self.name
    
    class Meta:
        ordering = ["name"]

class topic(models.Model):
    '''
    #####################################################
    # Represents a single topic record in the database. #
    # Known as 'Category' in the ui.                    #
    #####################################################
    '''
    id = uuidfield.UUIDField(auto=True, editable=False, primary_key=True)
    topic_name = models.CharField(max_length=100)
    topic_body = models.CharField(max_length=100, blank=True, null=True)
    moderator = models.ForeignKey(user, related_name='managesTopic')
    owner     = models.ForeignKey(user, related_name='ownsTopic')
    keyword_dict = models.CharField(max_length=1000, blank=True,null=True)
    content = models.ForeignKey(content, blank=True, null=True)
    is_locked = models.BooleanField()
    topic_group = models.ManyToManyField(group, through = 'topic_group')
    
    
    def __str__(self):
        return self.topic_name
    
class topic_group(models.Model):
    id = uuidfield.UUIDField(auto=True, editable=False, primary_key=True)
    topic = models.ForeignKey(topic, related_name='relatesGroup')
    group = models.ForeignKey(group, related_name='relatesTopic')

from hp.news.models import newsItem

class thread(models.Model):
    '''
    ###################################################################
    # Represents a single thread record in the database.              #
    # threads may be self-related to present a fully-nested heirarchy #
    ###################################################################
    '''
    id = uuidfield.UUIDField(auto=True, editable=False, primary_key=True)
    thread_name = models.CharField(max_length=100, blank=True, null=True)
    thread_body = models.CharField(max_length=500)
    datetime_created = models.DateTimeField(blank=True, null=True)
    keyword_dict = models.CharField(max_length=1000, blank=True, null=True)
    #add an Attachments table and relate to thread.
    content = models.ForeignKey(content, blank=True, null=True)
    topic = models.ForeignKey(topic)
    owner = models.ForeignKey(user)
    is_locked = models.BooleanField()
    parent_thread = models.ForeignKey('self', blank=True, null=True)
    parent_news = models.ForeignKey(newsItem, blank=True, null=True)
    thread_group = models.ManyToManyField(group, through = 'thread_group')
    most_popular = models.IntegerField()
    related_table = models.CharField(max_length=3)
    related_record_id = uuidfield.UUIDField()

    def __str__(self):
        return self.thread_name

class thread_group(models.Model):
    id = uuidfield.UUIDField(auto=True, editable=False, primary_key=True)
    thread = models.ForeignKey(thread, related_name='relatesGroup')
    group = models.ForeignKey(group, related_name='relatesThread')
    


