"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django import template


"""
# @author Muhammad Umair 
# e.g. << this is just as an sample, to get feedback.
# @author Muhammad Umair - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author Muhammad Umair - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""
register = template.Library()


def getXMLContentMenu(parser, token):
    try:    
        pass
        #tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return XMLContentMenu()

class XMLContentMenu(template.Node):
    def __init__(self):
        pass
    
    def render(self, context):
        xmlMenuHtml = '<div class="ency_cate_block">'
        xmlMenuHtml += '<a href="/28/000004/">Care Guides</a>'
        xmlMenuHtml += '<a href="/1/000001/">HIE Multimedia</a>'
        xmlMenuHtml += '<a href="/10/000001/">In-Depth Reports</a>'
        xmlMenuHtml += '<a href="/14/000005/">Pregnancy Center</a>'
        xmlMenuHtml += '</div>'
        xmlMenuHtml += '<div class="ency_cate_block">'
        xmlMenuHtml += '<a href="/49/150001/">Thomson Consumer Lab Database</a>'
        xmlMenuHtml += '<a href="/48/10001/">Thomson Alternative Medicine</a>'
        xmlMenuHtml += '<a href="/47/600003/">Thomson Detailed Drugs</a>'
        xmlMenuHtml += '<a href="/45/0001/">Thomson DrugNotes</a>'
        xmlMenuHtml += '</div>'
        return xmlMenuHtml
    
register.tag('getXMLContentMenu', getXMLContentMenu)

def length(value):
    try:
        return len(value)
    except (ValueError, TypeError):
        return ''
    length.is_safe = False

register.filter(length)