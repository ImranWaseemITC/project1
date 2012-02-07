"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.utils.html import strip_tags
from django.conf import settings
from hp.user.models import user as User
import datetime,uuid
#from hp.medicalcontent.classes.titleFinder import  titleFinder

from django.shortcuts import render_to_response

from hp.hp_utils import is_userLogged,isUserAction

"""
# @author Waqar Azeem
# e.g. << this is just as an sample, to get feedback.
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def homepage(request):
    """
    # URL recieved e.g. http://healthpark.ca/99/9999
    """
    user_status = is_userLogged(request)
    if user_status: 
        user_id = request.session['User_id']
    else: 
        user_id = ''   
    #Remove action     
    user_action = isUserAction(request);
    if user_action == True:
        action = request.session['Action']
        try:
            del request.session['Action']
        except:
            pass    
    else:
        action = ''          
    a = request.get_full_path()
    return render_to_response('home_content.html', {'user_isLogged':user_status, 'user_id':user_id,'path':a,'action':action}, context_instance=RequestContext(request))

"""
# @author Waqar Azeem
# e.g. << this is just as an sample, to get feedback.
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def aboutus(request):
    """
    # URL recieved e.g. http://healthpark.ca/99/9999
    """
    return render_to_response('aboutus.html',context_instance=RequestContext(request))

    
def send_email(request):
    feedback_message    = request.POST.get('feedback_text', '')
    feedback_type       = request.POST.getlist('type_feedback')
    user_id             = request.POST.get('user_id', '')
    page_url            = request.POST.get('path', '')
    redirect_url        = page_url
    email               = request.POST.get('email_address', '') 
    if feedback_message and feedback_type:
        message = "<br/>Hello,<br/>You have received a feedback with the details listed below:<br/>"
        if page_url == '/':
            page_url = 'www.healthpark.ca'
            message += "<b>Page URL:</b> "+page_url+"<br/>"
        else:
            page_url = 'www.healthpark.ca'+page_url
            message += "<b>Page URL:</b> "+page_url+"<br/>"
        if user_id:
            owner_user = User.objects.get(id=uuid.UUID(user_id))
            message += "<b>User ID:</b> "+user_id+"<br/>"
            if owner_user.first_name and owner_user.last_name:
                message += "<b>User Name:</b> "+owner_user.first_name+" "+owner_user.last_name+"<br/>" 
            if owner_user.first_name: 
                message += "<b>User Name:</b> "+owner_user.first_name+"<br/>"  
            message += "<b>User Email:</b> "+owner_user.email+"<br/>"
        if email and email != 'email address':
            message += "<b>User Email:</b> "+email+"<br/>"   
        message+= "<b>Feedback Message:</b> "+feedback_message+"<br/>"
        message+="<b>Feedback Type:</b> "+'\n'.join(feedback_type)+"<br/>"    
        try:
            text_content = strip_tags(message) 
            msg = EmailMultiAlternatives('User FeedBack',text_content,settings.FROM_EMAIL, [settings.TO_EMAIL])
            msg.attach_alternative( message, "text/html")
            msg.send()
        except BadHeaderError:
            #return HttpResponse('Invalid header found.')
            request.session['Action'] = 'system-error'
            return HttpResponseRedirect(redirect_url)
        request.session['Action'] = 'sent-feedback'
        return HttpResponseRedirect(redirect_url)
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        #return HttpResponse('Make sure all fields are entered and valid.')
        request.session['Action'] = 'user-error'
        return HttpResponseRedirect(redirect_url)


def refreshpage(request):
    """
    # URL recieved e.g. http://healthpark.ca/99/9999
    """
    user_status = is_userLogged(request)
    if user_status: 
        user_id = request.session['User_id']
    else: 
        user_id = ''   
    #Remove action     
    user_action = isUserAction(request);
    if user_action == True:
        action = request.session['Action']
        try:
            del request.session['Action']
        except:
            pass    
    else:
        action = ''          
    a = request.get_full_path()
    return render_to_response('page_refresh.html', {'user_isLogged':user_status, 'user_id':user_id,'path':a,'action':action}, context_instance=RequestContext(request))    
