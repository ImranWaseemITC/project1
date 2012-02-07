"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""

from django import template
from django.template import Context
from django.template.loader import get_template
from hp.dbfuncs import get_titlesubcontents
from hp.user.models import user as User
from hp.settings import MEDIA_URL 
register = template.Library()

"""
# @author Muhammad Imran
# e.g. << this method is to get titles of respective products and display them in Encyclopedia's body
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def getTitleofsubcontents(parser, token):
    try:    
        pass
        #tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return titleSubcontents()

class titleSubcontents(template.Node):
    def __init__(self):
        pass
 
    def Titlecontent(self,subcont):
        subcontent=subcont
        titlesubcontent=get_titlesubcontents(subcontent)
        Html='<div class="ency_box">'
        Html+='<form action="/searchByCategory/" method = "Post" class="cate_form"><span id="'+subcontent+'"></span>'
        Html+='<fieldset><input type="text" name ="search_input"  class="input_txt" onclick="get_csrf_token_for_category(\''+subcontent+'\')">'
        Html+= '<input type="hidden" name ="subcontent" value="'+subcontent+'"  class="input_txt">'
        Html+='<input type="submit" name ="search_button" value="Search this category " class="input_submit">'
        Html+='</fieldset></form>'
        Html+='<a href="/content/A?subcontent='+subcontent+'" class="btn_browse">Browse A-Z</a>'
        Html+='<div class="ency_cate_box"><div class="ency_cate_block">'
        count=0
        for item in titlesubcontent:
            if count< 4:
                Html+='<a href="/adamcontent/'+unicode(item[1])+'/'+unicode(item[2])+'/">'+unicode(item[0])+"</a>"
            count+=1    
            if count==4:            
                Html+='</div>'
                Html+='<div class="ency_cate_block">'
            if count>4 and count<8:
                Html+='<a href="/adamcontent/'+unicode(item[1])+'/'+unicode(item[2])+'/">'+unicode(item[0])+"</a>"
            if count==8:
                Html+='<a href="/adamcontent/'+unicode(item[1])+'/'+unicode(item[2])+'/">'+unicode(item[0])+"</a>"
                Html+='</div>'
                Html+='<div class="ency_cate_block">' 
            if count>8 and count<12:
                Html+='<a href="/adamcontent/'+unicode(item[1])+'/'+unicode(item[2])+'/">'+unicode(item[0])+"</a>"  
            
            if count==12:
                Html+='<a href="/adamcontent/'+unicode(item[1])+'/'+unicode(item[2])+'/">'+unicode(item[0])+"</a>"
                Html+='</div>'
                Html+='<div class="ency_cate_block last_ency_cate_block">'
            if count>12:
                Html+='<a href="/adamcontent/'+unicode(item[1])+'/'+unicode(item[2])+'/">'+unicode(item[0])+"</a>"
                                            
        Html+='</div></div></div>'    
        return Html
       
    def render(self, context):
        html=self.Titlecontent('Disease')
        html+=self.Titlecontent('Symptoms')
        html+=self.Titlecontent('Injury')
        html+=self.Titlecontent('Poison')
        html+=self.Titlecontent('Test')
        html+=self.Titlecontent('Surgery')
        html+=self.Titlecontent('Bloodless Medicine')
        html+=self.Titlecontent('Nutrition')
        html+=self.Titlecontent('drug')
        return html
register.tag('getTitleofsubcontents',getTitleofsubcontents)