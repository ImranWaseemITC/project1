from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from hp.admanager.forms import *
from hp.admanager.models import adclient as Adclient, internalad as Internalad, externalad as Externalad, adpool as Adpool
from django.utils.formats import get_format
from django.utils import formats
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.db.models import Q
import datetime
import uuid

"""
# @author Mohsin Aijaz
"""


def adManager(request):
    
    """
    # Provide interface for Ad-Manager
    """
    
    return render_to_response('admanager.html')

@csrf_protect
def createClient(request):
    
    """
    # Provide logic for creating Client if Client does'nt exist already
    """
    
    errors = []
   
    if request.method == 'POST':
        
        form = CreateAdClient(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            #check if client with the same name already exists or not
            try:
                
                x = Adclient.objects.get(name = cd['name'])
            
            #save if client with same name does'nt already exists
            except Adclient.DoesNotExist:
                
                try:
                    
                    p = Adclient(name = cd['name'], description = cd['description'])
                    p.save()
               
                except:
        
                    errors.append('Unable to save Ad Client!')
                    return render_to_response('createclient.html', 
                                              {'form': form, 'errors': errors}, 
                                              context_instance=RequestContext(request))
                
                return HttpResponseRedirect('/createclient/success/')
            
            if x:
               
                errors.append('Client already exists!')
                return render_to_response('createclient.html', 
                                          {'form': form, 'errors': errors}, 
                                          context_instance=RequestContext(request))
  
        else:
      
            return render_to_response('createclient.html', 
                                      {'form': form}, 
                                      context_instance=RequestContext(request))
    
    else:
   
        form = CreateAdClient()   
        return render_to_response('createclient.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))

def createClientSuccess(request):
    
    """
    # Display success page if client created successfully
    """
    
    return render_to_response('createclientsuccess.html')


@csrf_protect
def addInternalAd(request):
    
    """
    # Provide code for creating internal ads
    """
    
    errors = []
   
    if request.method == 'POST':
        
        form = AddInternalAd(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            
            if (cd['activeDate'] > cd['expiredDate']):
                
                errors.append('Expiry-date should be greater than Active-date!')
                return render_to_response('addinternalad.html', 
                                          {'form': form, 'errors': errors}, 
                                          context_instance=RequestContext(request))
            
            # saving internal ads
            try:

                p = Internalad(contentspecific = cd['contentSpecific'],
                               keywords = cd['keywords'],
                               activedate = cd['activeDate'],
                               expireddate = cd['expiredDate'],
                               noofimpressions = cd['noOfImpressions'],
                               priority = cd['priority'],
                               maximpressions = cd['maxImpressions'],
                               targetpages = cd['targetpages'],
                               ad = cd['ad'],
                               adtype = cd['adType'],
                               inoofimpressions = cd['noOfImpressions'],
                               campaignname = cd['campaignName']
                               )
                p.save()
               
            except:
        
                errors.append('Unable to save Internal Ad!')
                return render_to_response('addinternalad.html', 
                                          {'form': form, 'errors': errors}, 
                                          context_instance=RequestContext(request))
                
            return HttpResponseRedirect('/addinternalad/success/')
            
        else:
      
            return render_to_response('addinternalad.html', 
                                      {'form': form}, 
                                      context_instance=RequestContext(request))
    
    else:
   
        form = AddInternalAd()   
        return render_to_response('addinternalad.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))


@csrf_protect
def addExternalAd(request):
    
    """
    # Provide code for creating external ads
    """
    
    errors = []
   
    if request.method == 'POST':
        
        form = AddExternalAd(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            
            if (cd['activeDate'] > cd['expiredDate']):
                
                errors.append('Expiry-date should be greater than Active-date!')
                return render_to_response('addexternalad.html', 
                                          {'form': form, 'errors': errors}, 
                                          context_instance=RequestContext(request))
            
            # saving external ads
            try:
                    
                p = Externalad(adclient_id = cd['adclient_id'].id,
                               contentspecific = cd['contentSpecific'],
                               keywords = cd['keywords'],
                               activedate = cd['activeDate'],
                               expireddate = cd['expiredDate'],
                               noofimpressions = cd['noOfImpressions'],
                               priority = cd['priority'],
                               maximpressions = cd['maxImpressions'],
                               targetpages = cd['targetPages'],
                               adcode = cd['adCode'],
                               ad = cd['ad'],
                               adtype = str(cd['adType']),
                               inoofimpressions = cd['noOfImpressions'],
                               campaignname = cd['campaignName']
                               )
                p.save()
               
            except:
        
                errors.append('Unable to save Internal Ad!')
                return render_to_response('addexternalad.html', 
                                          {'form': form, 'errors': errors}, 
                                          context_instance=RequestContext(request))
                
            return HttpResponseRedirect('/addexternalad/success/')
            
        else:
   
            return render_to_response('addexternalad.html', 
                                      {'form': form}, 
                                      context_instance=RequestContext(request))
    
    else:
   
        form = AddExternalAd()   
        return render_to_response('addexternalad.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))

def createAdSuccess(request):
    
    """
    # Display success page if ad created successfully
    """
        
    return render_to_response('createadsuccess.html')

@csrf_protect
def createAdPool(request):
    
    """
    # Provide view for inserting campaign in ad-pool if it does'nt exist already
    """
    
    errors = []
   
    if request.method == 'POST':
        
        form = CreateAdPool(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            #check if campaign with the same name already exists or not
            try:
                
                x = Adpool.objects.get(campaignname = cd['campaignName'])
            
            #save if campaign with same name does'nt already exists
            except Adpool.DoesNotExist:
                
                try:
                    
                    p = Adpool(campaignname = cd['campaignName'], 
                               ad = cd['ad'], 
                               targetpages = cd['targetPages'],
                               adtype = cd['adType'])
                    p.save()
               
                except:
        
                    errors.append('Unable to save Ad in Pool!')
                    return render_to_response('createadpool.html', 
                                              {'form': form, 'errors': errors},
                                              context_instance=RequestContext(request))
                
                return HttpResponseRedirect('/createadpool/success/')
            
            if x:
               
                errors.append('Campaign already exists!')
                return render_to_response('createadpool.html', 
                                          {'form': form, 'errors': errors},
                                          context_instance=RequestContext(request))
  
        else:
  
            return render_to_response('createadpool.html', {'form': form},context_instance=RequestContext(request))
    
    else:
   
        form = CreateAdPool()   
        return render_to_response('createadpool.html', {'form': form},context_instance=RequestContext(request))

def createAdPoolSuccess(request):
    
    """
    # Display success page if ad inserted successfully in ad-pool
    """
    
    return render_to_response('createadpoolsuccess.html')

@csrf_protect
def deleteAds(request):
    
    """
    # Provide Logic for deleting ad(s)
    """
    
    if request.method == 'POST':
        
        form = DeleteAds(request.POST)
        
        if form.is_valid():
            
            cd = form.cleaned_data
            
            if cd['internalad_id'] or cd['externalad_id']:
            
                try:
                
                    #Delete Internal Ads
                    for eachInternalAd in cd['internalad_id']:
                        Internalad.objects.filter(id = eachInternalAd.id).delete()
                    
                    #Delete External Ads
                    for eachExternalAd in cd['externalad_id']:
                        Externalad.objects.filter(id = eachExternalAd.id).delete()
      
                except:
                    
                    error = 'Unable to Delete Ads!'
                    return render_to_response('deleteads.html', 
                                              {'form': form, 'error': error},
                                              context_instance=RequestContext(request))
                
                return HttpResponseRedirect('/deleteads/success/')
            
            else:
                
                error = 'Select ads to Delete!'
                return render_to_response('deleteads.html', 
                                              {'form': form, 'error': error},
                                              context_instance=RequestContext(request))
                
        else:
        
            return render_to_response('deleteads.html',
                                      {'form': form}, 
                                      context_instance=RequestContext(request))     
  
    else:
   
        form = DeleteAds()
           
        return render_to_response('deleteads.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))

def deleteAdsSuccess(request):
    
    """
    # Display success page when ad(s) deleted successfully
    """

    return render_to_response('deleteadssuccess.html', 
                              context_instance=RequestContext(request))
    
@csrf_protect
def editInternalAd(request):
    
    """
    # Provide logic for retrieving and updating internal ad
    """
    
    if request.method == 'POST':    
        
        form = EditInternalAd(request.POST)
        if form.is_valid():
           
            cd = form.cleaned_data
            
            #flag as if form is submitted by save button or form submitted by changing combobox
            if cd['myHiddenField'] == True:
                
                try:
                
                    #retrieve selected internal ad
                    
                    getInternalAd = Internalad.objects.get(id = cd['internalad_id'].id)                    
                    
                    form = EditInternalAd(initial={'internalad_id':getInternalAd,
                                                   'contentSpecific':getInternalAd.contentspecific,
                                                   'keywords':getInternalAd.keywords,
                                                   'activeDate':getInternalAd.activedate,
                                                   'expiredDate':getInternalAd.expireddate,
                                                   'noOfImpressions':getInternalAd.noofimpressions,
                                                   'priority':getInternalAd.priority,
                                                   'maxImpressions':getInternalAd.maximpressions,
                                                   'targetpages':getInternalAd.targetpages,
                                                   'ad':getInternalAd.ad,
                                                   'adType':getInternalAd.adtype
                                                   })
                    
                    return render_to_response('editinternalad.html', 
                                              {'form': form, 'myHiddenField':cd['myHiddenField']}, 
                                              context_instance=RequestContext(request))

                
                except:
                    
                    if not cd['internalad_id']:
                        
                            form = EditInternalAd()                       
                            
                            return render_to_response('editinternalad.html', {'form': form}, 
                              context_instance=RequestContext(request))
                    
                    error = 'Unable to retrieve internal ad!'
                    return render_to_response('editinternalad.html', 
                                              {'form': form, 'error': error}, 
                                              context_instance=RequestContext(request))                  
                                 
            
            else:
                
                #On  Save Update Internal ad
                try:
                
                    p = Internalad.objects.get(id = cd['internalad_id'].id)
    
                    p.contentspecific = cd['contentSpecific']
                    p.keywords = cd['keywords']
                    p.activedate = cd['activeDate']
                    p.expireddate = cd['expiredDate']
                    p.noofimpressions = cd['noOfImpressions']
                    p.priority = cd['priority']
                    p.maximpressions = cd['maxImpressions']
                    p.targetpages = cd['targetpages']
                    p.ad = cd['ad']
                    p.adtype = cd['adType']
                    p.inoofimpressions = cd['noOfImpressions']
                   
                    p.save()
                            
                except:
                        
                    error = error = 'Unable to save internal ad!'
                    return render_to_response('editinternalad.html', 
                                              {'form': form, 'error': error}, 
                                              context_instance=RequestContext(request))
                    
                return HttpResponseRedirect('/editinternalad/success/')    
            
        else:
        
            return render_to_response('editinternalad.html', 
                                      {'form': form}, 
                                      context_instance=RequestContext(request))              
    
    form = EditInternalAd()                       
    return render_to_response('editinternalad.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))
    
def editInternalAdSuccess(request):
    
    """
    # Display success page when internal ad updated successfully
    """

    return render_to_response('editinternaladsuccess.html', 
                              context_instance=RequestContext(request))

'''@csrf_protect
def editExternalAd(request):
    
    """
    # Provide logic for retrieving and updating external ad
    """
    
    if request.method == 'POST':    
        
        form = EditExternalAd(request.POST)
        if form.is_valid():
           
            cd = form.cleaned_data
            
            #flag as if form is submitted by save button or form submitted by changing combobox
            if cd['myHiddenField'] == True:
                
                try:
                
                    #retrieve selected external ad
                    
                    getExternalAd = Externalad.objects.get(id = cd['externalad_id'].id)                    
                    
                    form = EditExternalAd(initial={'externalad_id':getExternalAd,
                                                   'contentSpecific':getExternalAd.contentspecific,
                                                   'keywords':getExternalAd.keywords,
                                                   'activeDate':getExternalAd.activedate,
                                                   'expiredDate':getExternalAd.expireddate,
                                                   'noOfImpressions':getExternalAd.noofimpressions,
                                                   'priority':getExternalAd.priority,
                                                   'maxImpressions':getExternalAd.maximpressions,
                                                   'targetpages':getExternalAd.targetpages,
                                                   'ad':getExternalAd.ad,
                                                   'adType':getExternalAd.adtype,
                                                   'adCode':getExternalAd.adcode,
                                                   'adclient_id':getExternalAd.adclient,
                                                   })
                    
                    return render_to_response('editexternalad.html', 
                                              {'form': form, 'myHiddenField':cd['myHiddenField']}, 
                                              context_instance=RequestContext(request))

                
                except:
                    
                    if not cd['externalad_id']:
                        
                            form = EditExternalAd()                       
                            
                            return render_to_response('editexternalad.html', {'form': form}, 
                              context_instance=RequestContext(request))
                    
                    error = 'Unable to retrieve external ad!'
                    return render_to_response('editexternalad.html', 
                                              {'form': form, 'error': error}, 
                                              context_instance=RequestContext(request))                  
                                 
            
            else:
                
                #On  Save Update External ad
                try:
                
                    p = Externalad.objects.get(id = cd['externalad_id'].id)
    
                    p.contentspecific = cd['contentSpecific']
                    p.keywords = cd['keywords']
                    p.activedate = cd['activeDate']
                    p.expireddate = cd['expiredDate']
                    p.noofimpressions = cd['noOfImpressions']
                    p.priority = cd['priority']
                    p.maximpressions = cd['maxImpressions']
                    p.targetpages = cd['targetpages']
                    p.ad = cd['ad']
                    p.adtype = cd['adType']
                    p.inoofimpressions = cd['noOfImpressions']
                    p.adcode = cd['adCode']
                    p.adclient = cd['adclient_id'].id
                   
                    p.save()
                            
                except:
                        
                    error = error = 'Unable to save external ad!'
                    return render_to_response('editexternalad.html', 
                                              {'form': form, 'error': error}, 
                                              context_instance=RequestContext(request))
                    
                return HttpResponseRedirect('/editexternalad/success/')    
            
        else:
        
            return render_to_response('editexternalad.html', 
                                      {'form': form}, 
                                      context_instance=RequestContext(request))              
    
    form = EditExternalAd()                       
    return render_to_response('editexternalad.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))
    
def editExternalAdSuccess(request):
    
    """
    # Display success page when external ad updated successfully
    """

    return render_to_response('editexternaladsuccess.html', 
                              context_instance=RequestContext(request))'''

def checkAdPool(displaytype):
    
    try:
        
        # Checking ads all ads of current displaytype are displayed or not 
        adsToDisplay = Adpool.objects.filter(isdisplayed = False, adtype = displaytype)
           
        # If all ads are displayed, update impression counter in internal ads and external ads,
        # delete Adpool, and refill it
        if not adsToDisplay:
            
            # Get Distinct Internal ads from Adpool of current displaytype
            getInternalAdsFromAdPool = Adpool.objects.filter(adtype = displaytype).exclude(internalad = None).values('internalad').distinct().order_by('internalad')
            
            # For each Internal ad getting from Adpool, update it's impression counter in Internalad
            for eachAd in getInternalAdsFromAdPool:
                
                x = Internalad.objects.get(id = uuid.UUID(eachAd['internalad']))
                x.inoofimpressions = int(x.inoofimpressions) - int(x.priority)
                x.save()
            
            # Get Distinct External ads from Adpool of current displaytype
            getExternalAdsFromAdPool = Adpool.objects.filter(adtype = displaytype).exclude(externalad = None).values('externalad').distinct().order_by('externalad')
            
            # For each External ad getting from Adpool, update it's impression counter in Externalad
            for eachAd in getExternalAdsFromAdPool:
                
                x = Externalad.objects.get(id = uuid.UUID(eachAd['externalad']))
                x.inoofimpressions = int(x.inoofimpressions) - int(x.priority) 
                x.save()    
            
            # Delete all ads of current displaytype from Adpool 
            Adpool.objects.filter(adtype = displaytype).delete()
                
            # Refill Adpool
            
            # Get internal ads of current displaytype having active & expiry date greater than today,
            # and having impressioncounter > 0
                    
            getInternalAds = Internalad.objects.filter(
                                                       Q(activedate__gte = datetime.datetime.now()) | 
                                                       Q(expireddate__gte = datetime.datetime.now()) , 
                                                       Q(adtype = displaytype), 
                                                       Q(inoofimpressions__gt = 0)
                                                       ) 
            
            # Get external ads of current displaytype having active & expiry date greater than today,
            # and having impressioncounter > 0
            
            getExternalAds = Externalad.objects.filter(
                                                       Q(activedate__gte = datetime.datetime.now()) | 
                                                       Q(expireddate__gte = datetime.datetime.now()) , 
                                                       Q(adtype=displaytype), 
                                                       Q(inoofimpressions__gt = 0)
                                                       )
            
            # Fill internal ads in Adpool
            
            for eachAd in getInternalAds:
                
                for x in range(0,eachAd.priority):
                
                    p = Adpool(
                               campaignname = str(eachAd.campaignname),
                               ad = str(eachAd.ad),
                               targetpages = str(eachAd.targetpages),
                               adtype = str(eachAd.adtype),
                               internalad_id = uuid.UUID(eachAd.id)
                               )
                    
                    p.save()
                    
            # Fill external ads in Adpool
                
            for eachAd in getExternalAds:
                
                for x in range(0,eachAd.priority):
                
                    p = Adpool(
                               campaignname = str(eachAd.campaignname),
                               ad = str(eachAd.ad),
                               targetpages = str(eachAd.targetpages),
                               adtype = str(eachAd.adtype),
                               externalad_id = uuid.UUID(eachAd.id)
                               )
                    
                    p.save()
    
    except:
        
        pass                    