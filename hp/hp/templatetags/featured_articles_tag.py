"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django import template
from django.utils.html import strip_tags
from django.template import Context
from django.template.loader import get_template
from hp.dbfuncs import get_featuredContent
from hp.user.models import user as User
from xml.dom import minidom, Node
from django.conf import settings
from hp.settings import MEDIA_URL 
register = template.Library()

"""
# @author Muhammad Imran
# e.g. << this is to get product and its content and display them on featured Article's body.
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def getContents(parser, token):
    try:    
        pass
        #tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return featureArticle()

class featureArticle(template.Node):
    def __init__(self):
        pass
       
    def render(self, context):
        
        featuredcontent=get_featuredContent()
        xmlpath = settings.XML_ROOT.replace('\\','/')
        reviewby_list=[]
        html='<div class="article_slider">'
        html+='<ul>'
        for item in featuredcontent:
            prod=str(item[0])
            projid=str(item[1])
            genid=str(item[2])
	    imageid=str(item[3])
	    xmlfile  = xmlpath + "/" + prod + "/" + projid + "/"+genid+".xml"
            try:
                doc = minidom.parse(xmlpath + "/" + prod + "/" + projid + "/"+genid+".xml")
            except IOError:
                return 'Xml file:' + xmlfile  +' not found'
            for node in doc.getElementsByTagName("adamContent"):
                headerTitle = node.getAttribute("title")
                if node.nodeType == Node.ELEMENT_NODE:
                	headerSubContent = node.getAttribute("subContent")
            for txtcontnode in doc.getElementsByTagName("textContent"):
                #if txtcontnode.nodeType == Node.ELEMENT_NODE:
                    #title = txtcontnode.getAttribute("title")
                content = txtcontnode.toxml()
                content =  strip_tags(content)
                if len(content) > 150 :
                    content = content[:150]
                break
            for verinfo in doc.getElementsByTagName("versionInfo"):
                if verinfo.nodeType == Node.ELEMENT_NODE:
                    reviewdate=verinfo.getAttribute("reviewDate")
                    reviewby=verinfo.getAttribute("reviewedBy")
                    reviewby_list=reviewby.split(',')
                    reviewby=reviewby_list[0]+reviewby_list[1]
            html+='<li>'
            html+='<div class="art_img"><img src="/media/images/media/img_article'+imageid+'.jpg" width="360" height="269" alt=""></div>'
            html+='<div class="art_txt">'
            html+='<div class="art_title"><a href="/adamcontent/'+projid+'/'+genid+'/">'+headerTitle+'</a></div>'
            html+='<div class="art_date">'+reviewdate+'</div>'
            html+='<div class="art_info">'+reviewby+'|<a href="/adamcontent/'+projid+'/'+genid+'/">'+headerSubContent+'</a></div>'
            html+= content
            html+='<div class="art_links">'
            html+='<!--<a href="#" class="link_comment"><span>20</span>Comments</a>-->'
            html+='<a href="/adamcontent/'+projid+'/'+genid+'/" class="link_more">Read More</a>'
            html+='</div>'
            html+='</div>'
            html+='</li>'
 
        html+='</ul>'
        html+='</div>'  
        return html    
register.tag('getContents',getContents)
