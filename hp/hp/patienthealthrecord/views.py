from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from hp.patienthealthrecord.forms import *
from hp.patienthealthrecord.models import patienthealthrecord as Patienthealthrecord
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import uuid

"""
# @author Mohsin Aijaz
"""
@csrf_protect
def createPatientHealthRecord(request):
    
    """
    # Provide interface for creating Patient Health Record if User does'nt registered already
    """
    
    errors = []
   
    if request.method == 'POST':
        
        form = PatientHealthRecord(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            
            #check if user already registered or not
            try:
                
                x = Patienthealthrecord.objects.get(user = request.session['User_id'])
            
            #save if user does'nt already registered
            except Patienthealthrecord.DoesNotExist:
                
                try:
                    
                    p = Patienthealthrecord(provincialhealthid = cd['provincialHealthId'],
                                            address = cd['address'],
                                            city = cd['city'],
                                            province = cd['province'],
                                            postalcode = cd['postalCode'],
                                            dob = cd['dob'],
                                            gender = cd['gender'],
                                            user_id = uuid.UUID(request.session['User_id']))
                                                             
                    p.save()
               
                except:
        
                    errors.append('Unable to Registered!')
                    return render_to_response('createpatienthealthrecord.html',
                                               {'form': form, 'errors': errors}, 
                                               context_instance=RequestContext(request))
                
                return HttpResponseRedirect('/createpatienthealthrecord/success/')
            
            if x:
               
                errors.append('you already have a Profile!')
                return render_to_response('createpatienthealthrecord.html', 
                                          {'form': form, 'errors': errors},
                                          context_instance=RequestContext(request))
  
        else:
   
            form = PatientHealthRecord()   
            return render_to_response('createpatienthealthrecord.html', 
                                      {'form': form},
                                      context_instance=RequestContext(request))
    
    else:
   
        form = PatientHealthRecord()   
        return render_to_response('createpatienthealthrecord.html', {'form': form},context_instance=RequestContext(request))

def createPatientHealthRecordSuccess(request):
    
    return render_to_response('createpatienthealthrecordsuccess.html')

@csrf_protect
def managePatientHealthRecord(request):
    
    """
    # Provide interface for Updating/ Deleting Patient Health Record
    """
    
    errors = []
   
    if request.method == 'POST':

        if 'Update' in request.POST:
        
            form = PatientHealthRecord(request.POST)
            if form.is_valid():
                
                cd = form.cleaned_data
                
                
                try:
                    
                    p = Patienthealthrecord.objects.get(user = request.session['User_id'])
                    
                    p.provincialhealthid = cd['provincialHealthId']
                    p.address = cd['address']
                    p.city = cd['city']
                    p.province = cd['province']
                    p.postalcode = cd['postalCode']
                    p.dob = cd['dob']
                    p.gender = cd['gender']
                                                             
                    p.save()
               
                except:
        
                    errors.append('Unable to Update Patient Health Record!')
                    return render_to_response('managepatienthealthrecord.html',
                                               {'form': form, 'errors': errors}, 
                                               context_instance=RequestContext(request))
                
                return HttpResponseRedirect('/managepatienthealthrecord/')
            
                
            else:
     
                return render_to_response('managepatienthealthrecord.html', 
                                          {'form': form},
                                          context_instance=RequestContext(request))
        
        if 'Delete' in request.POST:
            
            try:
                
                Patienthealthrecord.objects.get(user = request.session['User_id']).delete()
                return HttpResponseRedirect('/deletepatienthealthrecord/success/')
            
            except:
    
                errors.append('Unable to Delete Profile!')
                return render_to_response('managepatienthealthrecord.html',
                                               {'form': form, 'errors': errors}, 
                                               context_instance=RequestContext(request))
    
    
    else:
        
        try:
             
            p = Patienthealthrecord.objects.get(user = request.session['User_id'])
             
        
            form = PatientHealthRecord(initial={'provincialHealthId':p.provincialhealthid,
                                                'address': p.address,
                                                'city': p.city,
                                                'province': p.province,
                                                'postalCode': p.postalcode,
                                                'dob': p.dob,
                                                'gender': p.gender
                                                })   
            
            return render_to_response('managepatienthealthrecord.html', {'form': form},context_instance=RequestContext(request))
        
        except Patienthealthrecord.DoesNotExist:
            
            return HttpResponseRedirect('/createpatienthealthrecord/')
        
        except:
    
            errors.append('Unable to Retrieve Patient Health Record!')
            return render_to_response('managepatienthealthrecord.html',
                                       {'form': form, 'errors': errors}, 
                                       context_instance=RequestContext(request))
        

def deletePatientHealthRecordSuccess(request):
    
    return render_to_response('deletepatienthealthrecordsuccess.html')