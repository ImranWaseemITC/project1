from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from hp.groupmanager.forms import *
from hp.groupmanager.models import group as Group,group_user as Group_User
from hp.user.models import user as User
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext


"""
# @author Mohsin Aijaz
"""

def groupManager(request):
    
    """
    # Provide interface for Group Manager
    """
    
    return render_to_response('centers.html',context_instance=RequestContext(request))

@csrf_protect
def createGroup(request):
    
    """
    # Provide logic for creating Group if group does'nt exist already
    """
    
    errors = [] 
   
    if request.method == 'POST':
        
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            
            #check if group with the same name already exists or not
            try:
                
                x = Group.objects.get(name = cd['name'])
            
            #save if group with same name does'nt already exists
            except Group.DoesNotExist:
                
                try:
                    
                    p = Group(name = cd['name'], description = cd['description'])
                    p.save()
               
                except:
        
                    errors.append('Unable to save Group!')
                    return render_to_response('creategroup.html', 
                                              {'form': form, 'errors': errors}, 
                                              context_instance=RequestContext(request))
                
                return HttpResponseRedirect('/creategroup/success/')
            
            if x:
               
                errors.append('Group already exists!')
                return render_to_response('creategroup.html', 
                                          {'form': form, 'errors': errors}, 
                                          context_instance=RequestContext(request))
        
        else:
            
            return render_to_response('creategroup.html', 
                                      {'form': form}, 
                                      context_instance=RequestContext(request))
          
    else:
   
        form = CreateGroupForm()   
        return render_to_response('creategroup.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))


@csrf_protect
def deleteGroup(request):
    
    """
    # Provide Logic for deleting Group(s)
    """
    
    if request.method == 'POST':
        
        form = DeleteGroupForm(request.POST)
        
        if form.is_valid():
            
            cd = form.cleaned_data
            
            try:
            
                #Delete records from m2m of Users & Groups for selected groups
                for eachGroup in cd['group_id']:
                    Group_User.objects.filter(group = eachGroup.id).delete()
                
                #Delete Group(s)
                for eachGroup in cd['group_id']:
                    Group.objects.filter(id = eachGroup.id).delete()
  
            except:
                
                error = 'Unable to Delete Groups!'
                return render_to_response('deletegroup.html', 
                                          {'form': form, 'error': error},
                                          context_instance=RequestContext(request))
            
            return HttpResponseRedirect('/deletegroup/success/')
        
        else:
        
            return render_to_response('deletegroup.html',
                                      {'form': form}, 
                                      context_instance=RequestContext(request))     
  
    else:
   
        form = DeleteGroupForm()
           
        return render_to_response('deletegroup.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))


@csrf_protect
def addUsersToGroup(request):
    
    """
    # Provide logic for retrieving and updating users in group
    """
    
    if request.method == 'POST':    
        
        form = AddUsersToGroupForm(request.POST)
        if form.is_valid():
           
            cd = form.cleaned_data
            
            #flag as if form is submitted by save button or form submitted by changing combobox
            if cd['myHiddenField'] == True:
                
                try:
                
                    #retrieve selected group with users
                    getUsersFromSelectedGroup=Group_User.objects.filter(group = cd['group_id'].id)
                    getFilteredUsers=User.objects.none()
                    
                    #retrieve selected group's users from user
                    for var in getUsersFromSelectedGroup:
                    
                        getFilteredUsers = getFilteredUsers | User.objects.filter(id=var.user_id) 
                    
                    form = AddUsersToGroupForm(initial={'user_id':getFilteredUsers, 'group_id':cd['group_id']})
                    
                    return render_to_response('addusers.html', 
                                              {'form': form, 'myHiddenField':cd['myHiddenField']}, 
                                              context_instance=RequestContext(request))
                
                except:
                    
                    error = 'Unable to save users in Group!'
                    return render_to_response('addusers.html', 
                                              {'form': form, 'error': error}, 
                                              context_instance=RequestContext(request))                  
                                 
            
            else:
                
                #On  Save Update Users of selected group
                try:
                
                    Group_User.objects.filter(group = cd['group_id'].id).delete()
                
                    for selectedUser in cd['user_id']:
                                
                            p = Group_User(group_id = cd['group_id'].id, user_id = selectedUser.id)
                            p.save()
                            
                except:
                        
                    error = 'Unable to save users in Group!'
                    return render_to_response('addusers.html', 
                                              {'form': form, 'error': error}, 
                                              context_instance=RequestContext(request))
                    
                return HttpResponseRedirect('/addusers/success/')    
            
        else:
        
            return render_to_response('addusers.html', 
                                      {'form': form}, 
                                      context_instance=RequestContext(request))              
    
    form = AddUsersToGroupForm()                       
    return render_to_response('addusers.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))
   
@csrf_protect
def success(request):
    
    """
    # Display success page when group created successfully
    """
    
    if request.method == 'POST':
        return HttpResponseRedirect('/creategroup/')
    
    return render_to_response('success.html', 
                              context_instance=RequestContext(request))

@csrf_protect
def addUsersSuccess(request):
    
    """
    # Display success page when user(s) in group updated successfully
    """
    
    if request.method == 'POST':
        return HttpResponseRedirect('/addusers/')
        
    return render_to_response('adduserssuccess.html', 
                              context_instance=RequestContext(request))

@csrf_protect
def deleteGroupSuccess(request):
    
    """
    # Display success page when group(s) deleted successfully
    """
    
    if request.method == 'POST':
        return HttpResponseRedirect('/deletegroup/')
    
    return render_to_response('deletegroupsuccess.html', 
                              context_instance=RequestContext(request))
   
      

      
  