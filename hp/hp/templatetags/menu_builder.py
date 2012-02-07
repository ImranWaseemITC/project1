"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django import template
from django.template import RequestContext
from django.db import connection


register = template.Library()


def menuBuilder(parser,token):
    try:
# split_contents() knows not to split quoted strings.
        pass
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return Menunode()

class Menunode(template.Node):
    def __init__(self):
        pass
    
    def render(self, context):
        cursor = connection.cursor()
        cursor.execute( 'SELECT * FROM getmenu()')
        queryset = cursor.fetchall()      
        menu_string="<ul>"
    
        for id,text,link,parent_id_id,depth,path in queryset:
            if depth == 1:
                    menu_string += '''<li><a href="''' + link + '''" class= "lev1">''' + text + '''</a><ul>'''
                    
                    for id1,text1,link1, parent_id_id1,depth1,path1 in queryset:
                        if depth1 == 2  and parent_id_id1 == id:
                            menu_string += '''<li><a href="'''+link1+'''" class="lev1">'''+ text1+'''</a><ul>'''    
                            
                            for id2,text2,link2,parent_id_id2,depth2,path2 in queryset:
                                if depth2 == 3  and parent_id_id2 == id1:
                                    menu_string +='''<li><a href="'''+link2+ '''" class="lev1">'''+text2+'''</a></li>'''
                            menu_string +='''</ul></li>'''
                    menu_string +='''</ul></li>'''
        menu_string +='''</ul>'''   
        
        return menu_string
                                
        
        #now = datetime.datetime.now()
        #return now.strftime(self.format_string)
    
register.tag('menuBuilder', menuBuilder)
