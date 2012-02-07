from django.db import models
import uuidfield
from hp.user.models import user
# Create your models here.

class userprofile(models.Model):
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    profilename = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    dob = models.DateField() 
    sex = models.CharField(max_length=50)
    bloodtype = models.CharField(max_length=50)
    ethinicity = models.CharField(max_length=50)
    user = models.ForeignKey(user)
    
    def __unicode__(self):
        return u'%s' % (self.profilename)
    class Meta:
        ordering = ["profilename"]
    
class personalprofile_phone(models.Model):   
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    phone = models.CharField(max_length=50) 
    phonetype = models.CharField(max_length=50) 
    userprofile = models.ForeignKey(userprofile)
    
class personalprofile_email(models.Model):   
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    email = models.CharField(max_length=50) 
    emailtype = models.CharField(max_length=50) 
    userprofile = models.ForeignKey(userprofile)
    
class personalprofile_adress(models.Model):   
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    adress = models.CharField(max_length=50)   
    adresstype = models.CharField(max_length=50)
    userprofile = models.ForeignKey(userprofile)
    
class familyhistory(models.Model):
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    condition = models.CharField(max_length=50)
    relation = models.CharField(max_length=50)
    relationshiptype = models.CharField(max_length=50)
    period = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    userprofile = models.ForeignKey(userprofile)   
    
class emergencycontacts(models.Model):
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    relationship = models.CharField(max_length=50)
    userprofile = models.ForeignKey(userprofile)
    
class emergencycontacts_phone(models.Model):   
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    phone = models.CharField(max_length=50) 
    phonetype = models.CharField(max_length=50) 
    emergencycontacts = models.ForeignKey(emergencycontacts)
    
class emergencycontacts_email(models.Model):   
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    email = models.CharField(max_length=50) 
    emailtype = models.CharField(max_length=50) 
    emergencycontacts = models.ForeignKey(emergencycontacts)
    
class emergencycontacts_adress(models.Model):   
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    adress = models.CharField(max_length=50)   
    adresstype = models.CharField(max_length=50)
    emergencycontacts = models.ForeignKey(emergencycontacts)
        
class socialhistory(models.Model):
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    maritalstatus = models.CharField(max_length=50)
    workconditions = models.CharField(max_length=2000)
    druguse = models.CharField(max_length=2000)
    physicalactivity = models.CharField(max_length=2000)
    userprofile = models.ForeignKey(userprofile)
