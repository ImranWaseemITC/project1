import uuidfield

from django.db import models

from hp.forum.models import topic

class newsItem(models.Model):
    """
    # Represents a single news object
    """
    id = uuidfield.UUIDField(auto = True, editable = False, primary_key = True)
    title = models.CharField(max_length = 100)
    summary = models.CharField(max_length = 500)
    body = models.TextField()
    topic = models.ForeignKey(topic)
    datetime_created = models.DateTimeField(blank=True, null=True)
    keyword_dict = models.CharField(max_length=1000, blank=True, null=True)
    author = models.CharField(max_length = 100)
    #image = models.ImageField(upload_to='images/news', blank=True)
    last_viewed = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return "%s" %self.title
    
    class Meta:
        ordering = ["title"]
        db_table = 'nws_item'