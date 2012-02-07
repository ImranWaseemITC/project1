import uuidfield
from django.db import models


#from hp.forum.models import thread

class hptb_attachments(models.Model):
    hptable_ID = models.CharField(max_length=4)
    hprecord_id=uuidfield.UUIDField(editable=False)
    docfile = models.FileField(upload_to='attachments')
    
    
    


'''    
    class Meta:
        hptb_attachments='hpa'
'''