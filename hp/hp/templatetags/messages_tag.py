"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django import template
from django.template import Context
from django.template.loader import get_template
from hp.user.models import user as User
from hp.admanager.models import adpool as Adpool
from hp.settings import MEDIA_URL 
from django.http import Http404,HttpResponse
from hp.admanager.models import *
from hp.admanager.views import *
import random
register = template.Library()
import psycopg2

"""
# @author Mohsin Aijaz, Fouzia Riaz, ...
"""



def getMessageContent(parser, token):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function for Latest Forum Content Displayed on Home Page
    """
    
    try:    
        pass   

    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return MessageContent(token.split_contents()[1],token.split_contents()[2])


class MessageContent(template.Node):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Class For Latest Forum Content Displayed on Home Page 
    """
    
    def __init__(self, msg_code, view_from_page):
        self.msg_code = template.Variable(msg_code)
        self.view_from_page = template.Variable(view_from_page)
        
    
    def render(self, context):
        msg_code = self.msg_code.resolve(context)
        view_from_page = self.view_from_page.resolve(context)
        #Post Messages
        if msg_code == 'add-post':
            message = 'Post Added Successfully.'
        elif msg_code == 'del-post':  
            message = 'Post Deleted Successfully.'  
        elif msg_code == 'edit-post':  
            message = 'Post Changed Successfully.'  
        elif msg_code == 'unlock-post':  
            message = 'Post Unlocked Successfully.'  
        elif msg_code == 'lock-post':  
            message = 'Post Locked Successfully.' 
        #Topic Messages    
        elif msg_code == 'edit-category':  
            message = 'Category Changed Successfully.' 
        elif msg_code == 'del-category':  
            message = 'Category Deleted Successfully.' 
        elif msg_code == 'unlock-category':  
            message = 'Category Unlocked Successfully.' 
        elif msg_code == 'lock-category':  
            message = 'Category Locked Successfully.'  
        #Feedback message
        if msg_code == 'sent-feedback':
            message = 'Thank you for your feedback.' 
        elif msg_code == 'system-error':
            message = 'Feedback sending failure due to system error.Please try again.'   
        elif msg_code == 'user-error':
            message = 'Feedback sending failure.Please try again.'            
        if view_from_page == 'home':
            class_name = 'success_message_home'
        elif view_from_page == 'forum': 
            class_name = 'success_message_forum'                                  
            
        show_message = '<div class="'+class_name+'"><span>'+message+'</span></div>'        
        return show_message

  
register.tag('getMessageContent', getMessageContent)


