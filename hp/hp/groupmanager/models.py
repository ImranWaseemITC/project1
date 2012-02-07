from django.db import models
import uuidfield
from hp.user.models import user

"""
# @author Mohsin Aijaz
"""


class group(models.Model):
    
    '''
    # The group Class defines group Object. It contains
    # group name and description
    '''
    
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    name = models.CharField(max_length=30)
    description = models.TextField(null = True, blank = True)
    user = models.ManyToManyField(user, null = True, blank = True, through='group_user') 
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        ordering = ["name"]
        
        
class group_user(models.Model):
    
    '''
    # The group_user Class will contain groups and it's 
    # users. It has a one-to-many relationship with group,        
    # and also a one-to-many relationship with User
    '''
    
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    group = models.ForeignKey(group)
    user = models.ForeignKey(user, null = True, blank = True)

