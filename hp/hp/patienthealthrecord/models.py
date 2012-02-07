from django.db import models
import uuidfield
from hp.user.models import user

class patienthealthrecord(models.Model):
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    user = models.ForeignKey(user, null = True, blank = True)
    provincialhealthid = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postalcode = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=50)
    
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        ordering = ["provincialhealthid"]
