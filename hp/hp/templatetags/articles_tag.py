"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""

from django import template
from django.template import Context
from django.template.loader import get_template
from hp.dbfuncs import get_articlescontent
from hp.user.models import user as User
from hp.settings import MEDIA_URL 
register = template.Library()

"""
# @author Muhammad Imran
# e.g. << This is just to get articles from database and display them on Home page
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def getArticleContents(parser, token):
    try:    
        pass
        #tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return ArticleContent()

class ArticleContent(template.Node):
    def __init__(self):
        pass
    
    def render(self, context):
        articlecontent = get_articlescontent()
        HtmlMenu=''
        for item,cont in articlecontent:
            HtmlMenu+='<li>'+str(cont)+'</li>'
        return HtmlMenu
  
register.tag('getArticleContents', getArticleContents)