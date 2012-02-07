from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from hp.phr.forms import *
from hp.phr.models import *
from hp.user.models import user as User
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from hp import hp_utils
import uuid

"""
# @author Mohsin Aijaz
"""

@csrf_protect
def addProfile(request):
    
    if hp_utils.is_userLogged(request):
    
        errors = [] 
       
        if request.method == 'POST':
            
            form6 = CreateEmergencyContacts(request.POST, prefix = 'form6')
            form7 = CreateEmergencyContacts_Phone(request.POST, prefix = 'form7')
            form8 = CreateEmergencyContacts_Email(request.POST, prefix = 'form8')
            form9 = CreateEmergencyContacts_Adress(request.POST, prefix = 'form9')
            
            if 'createprofile' in request.POST:
                
                num = 0
                form1 = CreatePersonalProfile(request.POST, prefix = 'form1')
                form2 = CreatePersonalProfile_Phone(request.POST, prefix = 'form2')
                form3 = CreatePersonalProfile_Email(request.POST, prefix = 'form3')
                form4 = CreatePersonalProfile_Adress(request.POST, prefix = 'form4')
            
                if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                    
                    cd1 = form1.cleaned_data
                    cd2 = form2.cleaned_data
                    cd3 = form3.cleaned_data
                    cd4 = form4.cleaned_data
                    
                    currentuser = User.objects.get(id = uuid.UUID(request.session["User_id"]))
                    
                    if cd1['myHiddenField']:
                        
                        p = userprofile.objects.get(id = cd1['myHiddenField'])
        
                        p.firstname = cd1['firstName']
                        p.middlename = cd1['middleName']
                        p.lastname = cd1['lastName']
                        p.dob =  cd1['dob']
                        p.sex = cd1['sex']
                        p.bloodtype = cd1['bloodType']
                        p.ethinicity = cd1['ethinicity']
                        p.save()
                        
                        p = personalprofile_phone.objects.get(userprofile = cd1['myHiddenField'])
                        p.phone =  cd2['phone']
                        p.phonetype =  cd2['phoneType']
                        p.save()
                        
                        p = personalprofile_email.objects.get(userprofile = cd1['myHiddenField'])
                        p.email =  cd3['email']
                        p.emailtype =  cd3['emailType']
                        p.save()
                        
                        p = personalprofile_adress.objects.get(userprofile = cd1['myHiddenField'])
                        p.adress =  cd4['adress']
                        p.adresstype =  cd4['adressType']
                        p.save()
                        
                        return HttpResponseRedirect('/phrprofiles?profile=' + cd1['myHiddenField'])
                    
                    else:
                    
                        try:
                        
                            personalprofile = userprofile.objects.get(profilename = cd1['profileName'], user = uuid.UUID(request.session["User_id"]))
                            
                        except userprofile.DoesNotExist:
                            
                            p = userprofile(
                                                   profilename = cd1['profileName'],
                                                   firstname = cd1['firstName'],
                                                   middlename = cd1['middleName'],
                                                   lastname = cd1['lastName'],
                                                   dob =  cd1['dob'],
                                                   sex = cd1['sex'],
                                                   bloodtype = cd1['bloodType'],
                                                   ethinicity = cd1['ethinicity'],
                                                   user = currentuser,
                                                   )
                            p.save()
                            x = p.id
                                
                            personalprofileid = userprofile.objects.get(id = uuid.UUID(x))
                            
                            p = personalprofile_phone(
                                                      phone =  cd2['phone'],
                                                      phonetype =  cd2['phoneType'],
                                                      userprofile = personalprofileid,
                                                      )
                            p.save()
                                
                            p = personalprofile_email(
                                                      email =  cd3['email'],
                                                      emailtype =  cd3['emailType'],
                                                      userprofile = personalprofileid,
                                                      )
                            p.save()
                                
                            p = personalprofile_adress(
                                                      adress =  cd4['adress'],
                                                      adresstype =  cd4['adressType'],
                                                      userprofile = personalprofileid,
                                                      )
                            p.save()   
                            
                            displaymsgt1 = []   
                            displaymsgt1.append('Profile created successfully!')   
                            
                            return HttpResponseRedirect('/phrprofiles?profile=' + personalprofileid.id) 
                                            
                        if personalprofile:
                              
                              displaymsgt1 = []   
                              displaymsgt1.append('hideit')
                              errors.append('Profile already exists!')
                              return render_to_response('createphrprofile.html', {'form1': form1,'form2': form2,'form3': form3,'form4': form4, 'num':num,'displaymsgt1':displaymsgt1[0],'errors': errors[0]}, context_instance=RequestContext(request))
                    
                else:
                    
                    displaymsgt1 = []   
                    displaymsgt1.append('hideit')
                    
                    return render_to_response('createphrprofile.html', {'form1': form1,'form2': form2,'form3': form3,'form4': form4, 'num':num,'displaymsgt1':displaymsgt1[0]}, context_instance=RequestContext(request))
                     
            if 'createemergencycontacts' in request.POST:
            
                num = 2
                if form6.is_valid() and form7.is_valid() and form8.is_valid() and form9.is_valid():
                    
                    cd6 = form6.cleaned_data
                    cd7 = form7.cleaned_data
                    cd8 = form8.cleaned_data
                    cd9 = form9.cleaned_data
                    
                    try:
                        
                        p = emergencycontacts.objects.get(id = cd6['myHiddenField2'])
                        p.relationship = cd6['relationship']
                        p.firstname = cd6['firstName']
                        p.middlename = cd6['middleName']
                        p.lastname = cd6['lastName']
                        p.save()
                        p = emergencycontacts_phone.objects.get(emergencycontacts = cd6['myHiddenField2'])
                        p.phone =  cd7['phone']
                        p.phonetype =  cd7['phoneType']
                        p.save()
                        p = emergencycontacts_email.objects.get(emergencycontacts = cd6['myHiddenField2'])
                        p.email =  cd8['email']
                        p.emailtype =  cd8['emailType']
                        p.save()
                        p = emergencycontacts_adress.objects.get(emergencycontacts = cd6['myHiddenField2'])
                        p.adress =  cd9['adress']
                        p.adresstype =  cd9['adressType']
                        p.save()
                        
                        return HttpResponseRedirect('/phrprofiles?profile=' + cd6['myHiddenField1'])
                    
                    except emergencycontacts.DoesNotExist:
                    
                        personalprofile = userprofile.objects.get(id = cd6['myHiddenField1'])
                        
                        p = emergencycontacts(
                                               relationship = cd6['relationship'],
                                               firstname = cd6['firstName'],
                                               middlename = cd6['middleName'],
                                               lastname = cd6['lastName'],
                                               userprofile = personalprofile,
                                               )
                        p.save()
                        x = p.id
                            
                        emergencycontact = emergencycontacts.objects.get(id = uuid.UUID(x))
                        
                        p = emergencycontacts_phone(
                                                    phone =  cd7['phone'],
                                                    phonetype =  cd7['phoneType'],
                                                    emergencycontacts = emergencycontact,
                                                    )
                        p.save()
                            
                        p = emergencycontacts_email(
                                                    email =  cd8['email'],
                                                    emailtype =  cd8['emailType'],
                                                    emergencycontacts = emergencycontact,
                                                    )
                        p.save()
                            
                        p = emergencycontacts_adress(
                                                     adress =  cd9['adress'],
                                                     adresstype =  cd9['adressType'],
                                                     emergencycontacts = emergencycontact,
                                                     )
                        p.save()   
                        
                        displaymsgt3 = []   
                        displaymsgt3.append('Emergency Contact created successfully!')    
                        
                        return HttpResponseRedirect('/phrprofiles?profile=' + cd6['myHiddenField1'])
                            
                else:
                    
                    return render_to_response('createphrprofile.html', {'form6': form6,'form7': form7,'form8': form8,'form9': form9, 'num':num}, context_instance=RequestContext(request)) 
    
                    
            if 'createfamilyhistory' in request.POST:
                
                num = 1
                form5 = CreateFamilyHistory(request.POST, prefix = 'form5')
        
                if form5.is_valid():
                    
                    cd5 = form5.cleaned_data
                        
                    try:
                        
                        p = familyhistory.objects.get(id = cd5['myHiddenField2'])
                        p.condition =  cd5['condition']
                        p.relation =  cd5['relation']
                        p.relationshiptype =  cd5['relationshipType']
                        p.period =  cd5['period']
                        p.gender =  cd5['gender']
                       
                        p.save()
                        
                        return HttpResponseRedirect('/phrprofiles?profile=' + cd5['myHiddenField1'])
                    
                    except familyhistory.DoesNotExist:    
                        
                        personalprofile = userprofile.objects.get(id = cd5['myHiddenField1'])
                                    
                        p = familyhistory(
                                      condition =  cd5['condition'],
                                      relation =  cd5['relation'],
                                      relationshiptype =  cd5['relationshipType'],
                                      period =  cd5['period'],
                                      gender =  cd5['gender'],
                                      userprofile = personalprofile,
                                      )
                        
                        p.save()
                        
                        displaymsgt2 = []   
                        displaymsgt2.append('Family history has created successfully!')                
                        
                        return HttpResponseRedirect('/phrprofiles?profile=' + cd5['myHiddenField1']) 
        
                else:
                
                    return render_to_response('createphrprofile.html', {'form5': form5, 'num':num}, context_instance=RequestContext(request)) 
                
            if 'createsocialhistory' in request.POST:
                
                num = 3
                form10 = CreateSocialHistory(request.POST, prefix = 'form10')
        
                if form10.is_valid():
                    
                    cd10 = form10.cleaned_data
                    
                    try:
                        
                        p = socialhistory.objects.get(userprofile = cd10['myHiddenField'])
                        p.maritalstatus =  cd10['maritalStatus']
                        p.workconditions =  cd10['workConditions']
                        p.druguse =  cd10['drugUse']
                        p.physicalactivity =  cd10['physicalActivity']
                       
                        p.save()
                        
                        return HttpResponseRedirect('/phrprofiles?profile=' + cd10['myHiddenField'])
                    
                    except socialhistory.DoesNotExist:    
                        
                        personalprofile = userprofile.objects.get(id = cd10['myHiddenField'])
                                    
                        p = socialhistory(
                                          maritalstatus =  cd10['maritalStatus'],
                                          workconditions =  cd10['workConditions'],
                                          druguse =  cd10['drugUse'],
                                          physicalactivity =  cd10['physicalActivity'],
                                          userprofile = personalprofile,
                                          )
                        p.save()
                        
                        displaymsgt4 = []   
                        displaymsgt4.append('Social history has created successfully!')    
                                        
                        return HttpResponseRedirect('/phrprofiles?profile=' + cd10['myHiddenField']) 
                    
                else:
                    
                    return render_to_response('createphrprofile.html', {'form10': form10, 'num':num}, context_instance=RequestContext(request))
     
    
        
        if request.method == 'GET':
            
            num = 0
            if 'profile' in request.GET:
                 
                 currentprofile = request.GET.get("profile")
                 personalProfile = userprofile.objects.get(id = currentprofile)

                 editform1 = CreatePersonalProfile(initial={
                                                       'myHiddenField':currentprofile,
                                                       'profileName':personalProfile.profilename,
                                                       'firstName':personalProfile.firstname,
                                                       'middleName':personalProfile.middlename,
                                                       'lastName':personalProfile.lastname,
                                                       'dob':personalProfile.dob,
                                                       'sex':personalProfile.sex,
                                                       'bloodType':personalProfile.bloodtype,
                                                       'ethinicity':personalProfile.ethinicity
                                                       }, prefix = 'form1')

                 
                 personalProfilePhone = personalprofile_phone.objects.get(userprofile = currentprofile)
                 
                 editform2 = CreatePersonalProfile_Phone(initial={
                                                       'phone':personalProfilePhone.phone,
                                                       'phoneType':personalProfilePhone.phonetype
                                                       }, prefix = 'form2')
                 
                 personalProfileEmail = personalprofile_email.objects.get(userprofile = currentprofile)
                 
                 editform3 = CreatePersonalProfile_Email(initial={
                                                       'email':personalProfileEmail.email,
                                                       'emailType':personalProfileEmail.emailtype
                                                       }, prefix = 'form3')
                 
                 personalProfileAdress = personalprofile_adress.objects.get(userprofile = currentprofile)
                 
                 editform4 = CreatePersonalProfile_Adress(initial={
                                                       'adress':personalProfileAdress.adress,
                                                       'adressType':personalProfileAdress.adresstype
                                                       }, prefix = 'form4')
             
                 
                 
                 return render_to_response('createphrprofile.html', {'form1': editform1,'form2': editform2,'form3': editform3,'form4': editform4, 'num':num},
                                          context_instance=RequestContext(request))
                 
            if 'familyprofile' in request.GET:
                
                 num = 1
                 currentprofile = request.GET.get("familyprofile")
                 
                 try:
                     
                     currentfamilyrecord = request.GET["familyrecord"]
                     
                     familyHistoryProfile = familyhistory.objects.get(id = currentfamilyrecord)
                     
                     editform5 = CreateFamilyHistory(initial={'myHiddenField1':currentprofile,
                                                              'myHiddenField2':currentfamilyrecord,
                                                              'condition':familyHistoryProfile.condition,
                                                              'relation':familyHistoryProfile.relation,                                                   
                                                              'relationshipType':familyHistoryProfile.relationshiptype,
                                                              'period':familyHistoryProfile.period,
                                                              'gender':familyHistoryProfile.gender
                                                               }, prefix = 'form5')
                     
                 except KeyError:
                     
                      familyHistoryProfile = familyhistory.objects.none()
                     
                      editform5 = CreateFamilyHistory(initial={'myHiddenField1':currentprofile}, prefix = 'form5')    
                 
                 return render_to_response('createphrprofile.html', {'form5': editform5, 'num':num},
                                          context_instance=RequestContext(request))
        
            if 'contactprofile' in request.GET:
                 
                num = 2
                currentprofile = request.GET.get("contactprofile")
                 
                try:
                     
                     currentcontactrecord = request.GET["contactrecord"]
                     
                     emergencyContactsProfile = emergencycontacts.objects.get(id = currentcontactrecord)
                     emergencyContactsPhone = emergencycontacts_phone.objects.get(emergencycontacts = currentcontactrecord)
                     emergencyContactsEmail = emergencycontacts_email.objects.get(emergencycontacts = currentcontactrecord)
                     emergencyContactsAdress= emergencycontacts_adress.objects.get(emergencycontacts = currentcontactrecord)
                     
                     editform6 = CreateEmergencyContacts(initial={'myHiddenField1':currentprofile,
                                                              'myHiddenField2':currentcontactrecord,
                                                              'firstName':emergencyContactsProfile.firstname,
                                                              'middleName':emergencyContactsProfile.middlename,                                                   
                                                              'lastName':emergencyContactsProfile.lastname,
                                                              'relationship':emergencyContactsProfile.relationship
                                                               }, prefix = 'form6')
                 
                     editform7 = CreateEmergencyContacts_Phone(initial={
                                                           'phone':emergencyContactsPhone.phone,
                                                           'phoneType':emergencyContactsPhone.phonetype
                                                           }, prefix = 'form7')
                     
                     editform8 = CreateEmergencyContacts_Email(initial={
                                                           'email':emergencyContactsEmail.email,
                                                           'emailType':emergencyContactsEmail.emailtype
                                                           }, prefix = 'form8')
                     
                     editform9 = CreateEmergencyContacts_Adress(initial={
                                                           'adress':emergencyContactsAdress.adress,
                                                           'adressType':emergencyContactsAdress.adresstype
                                                           }, prefix = 'form9')
                     
                except KeyError:
                     
                      editform6 = CreateEmergencyContacts(initial={'myHiddenField1':currentprofile}, prefix = 'form6')
                      editform7 = CreateEmergencyContacts_Phone(prefix = 'form7')
                      editform8 = CreateEmergencyContacts_Email(prefix = 'form8')
                      editform9 = CreateEmergencyContacts_Adress(prefix = 'form9')    
                 
                return render_to_response('createphrprofile.html', {'form6': editform6,'form7': editform7,'form8': editform8,'form9': editform9, 'num':num},
                                          context_instance=RequestContext(request))
         
            if 'socialprofile' in request.GET:
                 
                 num = 3
                 currentprofile = request.GET.get("socialprofile")
                 
                 try:
                 
                     socialHistoryProfile = socialhistory.objects.get(userprofile = currentprofile)
                     
                     editform10 = CreateSocialHistory(initial={'myHiddenField':currentprofile,
                                                               'maritalStatus':socialHistoryProfile.maritalstatus,
                                                               'workConditions':socialHistoryProfile.workconditions,                                                   
                                                               'drugUse':socialHistoryProfile.druguse,
                                                               'physicalActivity':socialHistoryProfile.physicalactivity
                                                               
                                                               }, prefix = 'form10')
                 
                 except socialhistory.DoesNotExist:
                     
                     socialHistoryProfile = socialhistory.objects.none()
                     
                     editform10 = CreateSocialHistory(initial={'myHiddenField':currentprofile}, prefix = 'form10')    
                 
                 return render_to_response('createphrprofile.html', {'form10': editform10, 'num':num},
                                          context_instance=RequestContext(request))
           
            else:
           
                form1 = CreatePersonalProfile(prefix = 'form1')
                form2 = CreatePersonalProfile_Phone(prefix = 'form2')
                form3 = CreatePersonalProfile_Email(prefix = 'form3')
                form4 = CreatePersonalProfile_Adress(prefix = 'form4')
                form5 = CreateFamilyHistory(prefix = 'form5')
                form6 = CreateEmergencyContacts(prefix = 'form6')
                form7 = CreateEmergencyContacts_Phone(prefix = 'form7')
                form8 = CreateEmergencyContacts_Email(prefix = 'form8')
                form9 = CreateEmergencyContacts_Adress(prefix = 'form9')
                form10 = CreateSocialHistory(prefix = 'form10') 
                
                displaymsgt1 = []   
                displaymsgt1.append('hideit') 
                num = 0
                return render_to_response('createphrprofile.html', {'form1': form1,'form2': form2,'form3': form3,'form4': form4,'form5': form5,'form6': form6,'form7': form7,'form8': form8,'form9': form9,'form10': form10,'num':num, 'displaymsgt1':displaymsgt1[0]}, context_instance=RequestContext(request))
    
    else:
        
        return HttpResponseRedirect('/')
    
@csrf_protect
def displayProfiles(request):
    
    if hp_utils.is_userLogged(request):
    
        if request.method == "GET":
          
            if request.GET.get("profile"):
                
                profile = request.GET.get("profile")
                personalProfile = userprofile.objects.get(id = uuid.UUID(profile))
                
                try:
                    
                    socialHistory = socialhistory.objects.get(userprofile = personalProfile.id)
                
                except socialhistory.DoesNotExist:
                    
                    socialHistory = socialhistory.objects.none()
                    
                familyHistory = familyhistory.objects.filter(userprofile = personalProfile.id).values_list('id','condition','period','gender','relation','relationshiptype')
                
                try:
                    
                    personalProfilePhone = personalprofile_phone.objects.get(userprofile = personalProfile.id)
                
                except socialhistory.DoesNotExist:
                    
                    personalProfilePhone = personalprofile_phone.objects.none()
                
                try:
                    
                    personalProfileEmail = personalprofile_email.objects.get(userprofile = personalProfile.id)
                
                except socialhistory.DoesNotExist:
                    
                    personalProfileEmail = personalprofile_email.objects.none()
                
                try:
                    
                    personalProfileAdress = personalprofile_adress.objects.get(userprofile = personalProfile.id)
                
                except socialhistory.DoesNotExist:
                    
                    personalProfileAdress = personalprofile_adress.objects.none()
                
                emergencyContacts = emergencycontacts.objects.filter(userprofile = personalProfile.id)
                emergencyContactsPhone = []
                emergencyContactsEmail = []
                emergencyContactsAdress = []
                
                for ec in emergencyContacts:
                    
                    try:
                    
                        emergencyContactsPhone.extend(emergencycontacts_phone.objects.filter(emergencycontacts = ec.id).values_list())
                
                    except emergencycontacts_phone.DoesNotExist:
                        
                        emergencyContactsPhone.extend(emergencycontacts_phone.objects.none().values_list())
                    
                    try:
                    
                        emergencyContactsEmail.extend(emergencycontacts_email.objects.filter(emergencycontacts = ec.id).values_list())
                
                    except emergencycontacts_email.DoesNotExist:
                        
                        emergencyContactsEmail.extend(emergencycontacts_email.objects.none().values_list())
                    
                    try:
                    
                        emergencyContactsAdress.extend(emergencycontacts_adress.objects.filter(emergencycontacts = ec.id).values_list())
                
                    except socialhistory.DoesNotExist:
                        
                        emergencyContactsAdress.extend(emergencycontacts_adress.objects.none().values_list())
                        
                    emergencyContacts = emergencycontacts.objects.filter(userprofile = personalProfile.id).values_list()
                    
 
                return render_to_response('phrprofile.html', {'personalProfile':personalProfile, 
                                                              'socialHistory':socialHistory, 
                                                              'familyHistory':familyHistory, 
                                                              'personalProfilePhone':personalProfilePhone, 
                                                              'personalProfileEmail':personalProfileEmail, 
                                                              'personalProfileAdress':personalProfileAdress, 
                                                              'emergencyContacts':emergencyContacts, 
                                                              'emergencyContactsPhone':emergencyContactsPhone, 
                                                              'emergencyContactsEmail':emergencyContactsEmail, 
                                                              'emergencyContactsAdress':emergencyContactsAdress},
                                          context_instance=RequestContext(request))
                    
            else:        
                
                phrprofiles = userprofile.objects.filter(user = uuid.UUID(request.session["User_id"]))
                currentuser = User.objects.get(id = uuid.UUID(request.session["User_id"]))
                
                return render_to_response('phrprofiles.html', {'phrprofiles':phrprofiles, 'currentuser':currentuser}, context_instance=RequestContext(request))
        
        if request.method == "POST":
             
             if 'deleteprofile' in request.POST:
             
                 currentprofile = request.POST.get("currentprofile")
                 userprofile.objects.filter(id = currentprofile, user = uuid.UUID(request.session["User_id"])).delete()
                 
                 return HttpResponseRedirect('/phrprofiles')
             
    else:
        
        return HttpResponseRedirect('/')
             
         
         