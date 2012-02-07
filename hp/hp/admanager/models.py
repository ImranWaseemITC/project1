from django.db import models
import uuidfield

"""
# @author Mohsin Aijaz
"""

class adclient(models.Model):
    
    '''
    # The adclient Class will contain Client Object.
    # It contains Client name & description.
    '''
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    name = models.CharField(max_length=30)
    description = models.TextField(null = True, blank = True)

    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        ordering = ["name"]
        
class internalad(models.Model):
    
    '''
    # The 'internalad' Class contains Ad object, managed by us.
    # targetpages: URL where this Ad will be displayed
    # priority: frequency or occurrence of an Ad in pool
    # impressions: total number of occurrence i.e. life of an Ad
    # ad: Ad script/HTML
    '''
    
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    campaignname = models.CharField(max_length=30)
    contentspecific = models.CharField(max_length=30)
    keywords = models.CharField(max_length=30)
    activedate = models.DateField()
    expireddate = models.DateField()
    noofimpressions = models.IntegerField()
    priority = models.IntegerField()
    maximpressions = models.IntegerField()
    targetpages = models.TextField()
    adtype = models.CharField(max_length=30)
    ad = models.TextField()
    inoofimpressions = models.IntegerField(null = True)
    
    def __unicode__(self):
        return u'%s' % (self.campaignname)
    class Meta:
        ordering = ["campaignname"]

class externalad(models.Model):
    
    '''
    # The 'externalad' Class contains Ad object, managed by us.
    # targetpages: URL where this Ad will be displayed
    # priority: frequency or occurrence of an Ad in pool
    # impressions: total number of occurrence i.e. life of an Ad
    # ad: Ad script/HTML
    # adclient: ad provider i.e. hp client
    # adcode: ad code provided by hp client
    '''
    
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    campaignname = models.CharField(max_length=30)
    adclient = models.ForeignKey(adclient)
    contentspecific = models.CharField(max_length=30)
    keywords = models.CharField(max_length=30)
    activedate = models.DateField()
    expireddate = models.DateField()
    noofimpressions = models.IntegerField()
    priority = models.IntegerField()
    maximpressions = models.IntegerField()
    targetpages = models.TextField()
    adtype = models.CharField(max_length=30)
    adcode = models.CharField(max_length=30)
    ad = models.TextField()
    inoofimpressions = models.IntegerField(null = True)
    
    def __unicode__(self):
        return u'%s' % (self.campaignname)
    class Meta:
        ordering = ["campaignname"]
    
class adpool(models.Model):
    
    '''
    # The adpool Class will contain ad object,
    # the class is temporary created to fill
    # ad pool manually
    '''
    
    id = uuidfield.UUIDField(primary_key = True, auto=True, editable = False)
    internalad = models.ForeignKey(internalad)
    externalad = models.ForeignKey(externalad)
    campaignname = models.CharField(max_length=30)
    ad = models.TextField()
    targetpages = models.TextField()
    adtype = models.CharField(max_length=30)
    isdisplayed = models.BooleanField()

