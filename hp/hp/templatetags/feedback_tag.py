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
from hp.forum.models import thread as Thread
from hp.settings import MEDIA_URL 
from django.http import Http404,HttpResponse
from django.utils.safestring import mark_safe
from hp.feedback.forms import feedback_form
register = template.Library()



def getFeedbackForm(parser, token):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Getting Feedback Form
    """
    
    try:    
        pass

    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return FeedbackForm(token.split_contents()[1],token.split_contents()[2],token.split_contents()[3])


class FeedbackForm(template.Node):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Class for For Getting Feedback Form
    """
    def __init__(self, user_isLogged, owner, path):
       self.user_isLogged  = template.Variable(user_isLogged)
       self.owner  = template.Variable(owner)
       self.path  = template.Variable(path)
    
    def render(self, context):
        user_isLogged = self.user_isLogged.resolve(context)
        owner = self.owner.resolve(context)
        path = self.path.resolve(context)
        feedbackForm = feedback_form(initial = {'user_id':owner,'path':path})
        return feedbackForm
       
register.tag('getFeedbackForm', getFeedbackForm)
