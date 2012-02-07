"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django import template
from django.template import Context
from django.template.loader import get_template
from hp.dbfuncs import get_latest_threads, get_active_categories, get_topic_threads, get_threads_by_id,get_news_top_thread
from hp.user.models import user as User
from hp.forum.models import thread as Thread
from hp.settings import MEDIA_URL 
from django.http import Http404,HttpResponse
from django.utils.safestring import mark_safe
register = template.Library()

def getForumActivityContext(forum_row, is_topic, topic_count, user_isLogged, owner, topic_is_locked):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Forum Activity Context Required In ForumActivity Class 
    """ 
    view_page = '';
    if is_topic == 'true' or topic_is_locked == "null":
        if topic_is_locked == "null":
            view_page = 'view-all-forum' 
        thread_date = forum_row[9]
        thread_time = forum_row[10]
        most_popular = forum_row[7]
        if forum_row[9] is None or forum_row[9] <= 0:
            thread_date = '0'  
        if forum_row[10] is None or forum_row[10] <= 0:
            thread_time = '0'                
        if forum_row[8] > 0:
            thread_count = forum_row[8]-1
        elif forum_row[8] == 0:
            thread_count = forum_row[8] 
        if owner == forum_row[14]:
            display_activity_links = 'true'
        elif owner != forum_row[14]:
            display_activity_links = 'false'
        if forum_row[15]:
            is_locked = True
        else:
            is_locked = False            
    else:  
        thread_date = forum_row[6]
        thread_time = forum_row[7]
        most_popular = forum_row[8]
        if forum_row[6] is None or forum_row[6] <= 0:
            thread_date = '0'  
        if forum_row[7] is None or forum_row[7] <= 0:
            thread_time = '0'                
        if forum_row[5] > 0:
            thread_count = forum_row[5]-1
        elif forum_row[5] == 0:
            thread_count = forum_row[5]  
        if owner == forum_row[11]:
            display_activity_links = 'true'
        elif owner != forum_row[11]:
            display_activity_links = 'false' 
        if forum_row[12]:
            is_locked = True
        else:
            is_locked = False    
                          
    forum_context = {'id':forum_row[0],'thread_count':thread_count,'thread_date':thread_date,'thread_time':thread_time,'first_name':forum_row[3],'last_name':forum_row[4],'thread_topic':forum_row[1],'thread_body':mark_safe(forum_row[2]),'topic_count':topic_count,'topic_id':forum_row[11],'most_popular':most_popular, 'user_isLogged':user_isLogged, 'owner':owner,'topic_is_locked': topic_is_locked,'display_activity_links':display_activity_links,'is_locked':is_locked,'view_page':view_page}    
    return forum_context

def getForumThreadContext(thread_row,thread_list,topic_id,thread_id,div_type,div_id,user_isLogged, reply_form, owner_id, is_locked):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Thread Context Required In ForumActivityThread Class 
    """ 
    thread_date = thread_row[9]
    thread_time = thread_row[10]
    if topic_id:
        if div_type == 'parent':
            div_type = 1            #1 = parent forum-thread need to be display in case of forum
    else:
        if div_type == 'parent':
            div_type = 0 
            #div_type = 2            #0 = parent forum-thread need to be display in case of news    
    if div_type == 'child':
        div_type = 2            #2 = Immediate child 
    elif div_type == 'sub_child': 
        div_type = 3            #3 = grant children
    if thread_row[9] is None or thread_row[9] <= 0:
            thread_date = '0'  
    if thread_row[10] is None or thread_row[10] <= 0:
            thread_time = '0'      
    if owner_id == thread_row[13]:
        display_activity_links = 'true'
    elif owner_id != thread_row[13]:
        display_activity_links = 'false' 
    if not thread_list is None:                     
        thread_count = len(thread_list)
    else:  
        thread_count = 0   
    thread_context = {'id':thread_row[0],'thread_count':thread_count-1,'topic_id':topic_id,'thread':thread_id,'div_type':div_type,'div_id':div_id,'thread_title':thread_row[1],'thread_body':mark_safe(thread_row[2]),'first_name':thread_row[3],'last_name':thread_row[4],'user_isLogged':user_isLogged,'reply_form':reply_form,'most_popular':thread_row[12],'thread_time':thread_time,'thread_date':thread_date,'display_activity_links':display_activity_links,'is_locked':is_locked}
    return thread_context

def getForumActivityContent(parser, token):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Forum Activity Displayed on Forum  Page 
    """ 
    
    try:    
        pass
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    #return ForumActivity()
    return ForumActivity(token.split_contents()[1], token.split_contents()[2], token.split_contents()[3], token.split_contents()[4])

class ForumActivity(template.Node):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Class For Forum Activity Displayed on Forum  Page 
    """
    def __init__(self, category, user_isLogged, owner, topic_is_locked ):
        self.category           = template.Variable(category)
        self.user_isLogged      = template.Variable(user_isLogged)
        self.owner              = template.Variable(owner)
        self.topic_is_locked    = template.Variable(topic_is_locked)
    
    def render(self, context):
        category_id             = self.category.resolve(context)
        user_isLogged           = self.user_isLogged.resolve(context)
        owner                   = self.owner.resolve(context)
        topic_is_locked         = self.topic_is_locked.resolve(context)
        try:
            if len(category_id) == 0:
                forumActivityContent = get_latest_threads("mostpopular", "limit 5")
                forumActivityCount = get_latest_threads("mostpopular", "")
                topic_count = len(forumActivityCount)
                is_topic = 'false'
            else:
                if category_id != 'none':
                    forumActivityContent = get_topic_threads(category_id, "mostpopular", "limit 5")
                    forumActivityCount = get_topic_threads(category_id, "mostpopular", "")
                    
                else:
                    category_id = "null"
                    forumActivityContent = get_topic_threads(category_id, "mostpopular", "limit 5")
                    forumActivityCount = get_topic_threads(category_id, "mostpopular", "")
                    topic_is_locked = "null"
                is_topic = 'true'
                topic_count = len(forumActivityCount)
                
                
            forum_activity = ''
            if len(forumActivityContent) > 0:
                for forum_row in forumActivityContent:
                    if is_topic == 'true':
                        forum_context = getForumActivityContext(forum_row, is_topic, topic_count, user_isLogged, owner, topic_is_locked)
                    else:
                        forum_context = getForumActivityContext(forum_row, is_topic, topic_count, user_isLogged, owner, topic_is_locked)
                    forum_template = get_template('home_forumContent.html')
                    forum_activity += forum_template.render(Context(forum_context))      
            elif len(forumActivityContent) == 0:
                forum_activity+= '<br/><br/><center><i>No records found.</i></center></br/></br/>'
            if len(category_id) != 0:
                forum_activity += '<input type="hidden" value="'+category_id+'" id="cat_id"/>'
            forum_activity += '<input type="hidden" value="'+`topic_count`+'" id="topic_count"/><input type="hidden" value="mostpopular" id="order_by"/>'                    
            return forum_activity
        except:
            forum_activity = '<br/><br/><center><i>No Records Found</i></center><br/><br/><br/>'
            return forum_activity

register.tag('getForumActivityContent', getForumActivityContent)

def getForumActivityThreads(parser, token):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Forum Activity Displayed on Forum  Threads Page 
    """ 
    
    try:    
        pass
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return  ForumActivityThreads(token.split_contents()[1],token.split_contents()[2],token.split_contents()[3],token.split_contents()[4],token.split_contents()[5])

class ForumActivityThreads(template.Node):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Class For Forum Activity Displayed on Forum  Threads Page  
    """
    def __init__(self, category, thread, user_isLogged, reply_form, owner_id):
        self.category = template.Variable(category)
        self.thread = template.Variable(thread)
        self.user_isLogged = template.Variable(user_isLogged)
        self.reply_form = template.Variable(reply_form)
        self.owner_id   = template.Variable(owner_id)
    def render(self, context):
        category_id = self.category.resolve(context)
        thread_id = self.thread.resolve(context)
        user_isLogged = self.user_isLogged.resolve(context)
        reply_form = self.reply_form.resolve(context)
        owner_id    =self.owner_id.resolve(context)
        if category_id: 
            threadsList = get_threads_by_id(thread_id)
        else:
            threadList = get_news_top_thread(thread_id)
            threadsList = get_threads_by_id(threadList[0][0])
        row = 0; sub_child = 0; child = 0;parent_node = "";forum_thread = "";thread_context = "";padding_start_div="";padding_end_div="";current_parent_node="";is_locked = False
        if len(threadsList) > 0:
            for thread_row in threadsList:
                current_parent_id = str(thread_row[5])
                #PARENT DISPLAY
                if thread_row[5] is None:
                    parent_node = str(thread_row[0]); div_id = ""; child = child+1
                    if thread_row[14]:
                        is_locked = True
                    else:
                        is_locked = False   
                   
                    if category_id: 
                        thread_context = getForumThreadContext(thread_row,threadsList,category_id,thread_id,'parent',div_id,user_isLogged, reply_form, owner_id, is_locked)
                        thread_template = get_template('forum_threadContent.html')
                        forum_thread += thread_template.render(Context(thread_context)) 
                    else:
                        div_id = "divs";
                        thread_context = getForumThreadContext(thread_row,threadsList,None,thread_id,'parent',div_id,user_isLogged, reply_form, owner_id, is_locked)
                        thread_template = get_template('forum_threadContent.html')      
                        forum_thread = thread_template.render(Context(thread_context))
                        forum_thread +='<ul><li>' 
                        #child = child+1; sub_child = 2;      
                if not thread_row[5] is None:
                    previous_content_id = str(threadsList[row-1][0])
                    current_parent_id = str(thread_row[5])
                    #SUB CHILD DISPLAY
                    if (previous_content_id == current_parent_id and current_parent_id != parent_node)or current_parent_id == current_parent_node:     
                       
                        if sub_child == 1 or current_parent_id == current_parent_node:
                            if sub_child == 1:
                                div_id = div_id + "-div"+`sub_child`
                            if current_parent_id == current_parent_node:
                                div_id = "divs"+`child-1` + "-div"+`sub_child`    
                            thread_context = getForumThreadContext(thread_row,threadsList,category_id,thread_id,'sub_child',div_id,user_isLogged,'', owner_id, is_locked)
                            thread_template = get_template('forum_threadContent.html')
                            forum_thread += thread_template.render(Context(thread_context)) 
                        elif sub_child > 1:
                            div_id = div_id + "-div"+`sub_child`
                            forum_thread +='<ul><li>'
                            thread_context = getForumThreadContext(thread_row,threadsList,category_id,thread_id,'sub_child',div_id,user_isLogged,'', owner_id, is_locked)
                            thread_template = get_template('forum_threadContent.html')
                            forum_thread += thread_template.render(Context(thread_context))
                            forum_thread +='</li></ul>' 
                    #CHILD DISPLAY    
                    elif (previous_content_id != current_parent_id or current_parent_id == parent_node) and current_parent_id != current_parent_node:     
                        div_id = "divs"+`child`; child = child+1; sub_child = 0;current_parent_node = str(thread_row[0])
                        thread_context = getForumThreadContext(thread_row,threadsList,category_id,thread_id,'child',div_id,user_isLogged,'', owner_id, is_locked)
                        thread_template = get_template('forum_threadContent.html')
                        forum_thread += thread_template.render(Context(thread_context))            
                sub_child = sub_child + 1       
                row = row + 1           
            #forum_thread += '</li><li><div class="load_more"><a href="#">[ + ]   Load more comments</a> ('+`len(threadsList)-1`+' replies)</div></li></ul></div>'
            if category_id:
                forum_thread += '</li><li><div class="load_more"></div></li></ul></div>'
            else: 
                 forum_thread += '</li></ul></li></ul></div>'   
        elif len(threadsList) == 0:
            forum_thread += '<br/><br/><center><i>No records found.</i></center></br/></br/>'
        return forum_thread 
register.tag('getForumActivityThreads', getForumActivityThreads)

def getCategories(parser, token):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Active Categories Displayed on Home Page
    """
    
    try:    
        pass

    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return AllCategories(token.split_contents()[1],token.split_contents()[2],token.split_contents()[3],token.split_contents()[4],token.split_contents()[5],token.split_contents()[6])


class AllCategories(template.Node):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Class for Active Categories Displayed on Home Page
    """
    def __init__(self, user_isLogged, user_id, topic_id, topic_is_locked,thread_id, data_limit):
        self.user_isLogged      = template.Variable(user_isLogged)
        self.user_id            = template.Variable(user_id)
        self.topic_id           = template.Variable(topic_id)
        self.topic_is_locked    = template.Variable(topic_is_locked)
        self.thread_id    = template.Variable(thread_id)
        self.data_limit    = template.Variable(data_limit)
    
    def render(self, context):
        user_isLogged       = self.user_isLogged.resolve(context)
        user_id             = self.user_id.resolve(context) 
        topic_id            = self.topic_id.resolve(context)
        topic_is_locked     = self.topic_is_locked.resolve(context)
        thread_id           = self.thread_id.resolve(context)
        data_limit           = self.data_limit.resolve(context)
        
        if not data_limit is None:
            activeCategories = get_active_categories(data_limit)
        elif data_limit is None:
            activeCategories = get_active_categories('')    
        active_categories = ''
        if len(activeCategories) > 0:
            for category_row in activeCategories:  
                if topic_id == category_row[0]:
                    style = 'style = "color:#8AAA3F"'
                else:
                    style=''      
                #active_categories += '<li><span onclick="getForumContentByTopic(\''+category_row[0]+'\')" class="ac_cat_list">'+category_row[1].capitalize()+'</span></li>'
                if len(category_row[1]) > 10:
                    category_title = category_row[1][0:15]+'...'
                else:
                    category_title = category_row[1]
                active_categories += '<li>'
                active_categories += '<a href="/forum/?cat_id='+category_row[0]+'/" class="ac_cat_list" title="'+category_row[1]+'" '+style+'>'+category_title+'</a>'
                if user_isLogged:
                    if category_row[4] == user_id:
                        if category_row[7]:
                            append_link = 'unlock'
                        else:
                            append_link = 'lock'
                        if not thread_id is None:
                            thread_link_id = "/" + thread_id
                        else:
                            thread_link_id = "/"             
                        if len(data_limit)> 0:
                            active_categories += '<span id="edit_link_span"><a href="/forum/editcategory/'+category_row[0]+'/'+topic_id+thread_link_id+'" title="Click to edit category"><img src="/media/images/edit-icon.jpeg"/></a>  <a href="/'+append_link+'topic/'+ category_row[0] +'/'+ topic_id +'/True"><img src="/media/images/'+append_link+'-icon.png"/></a>  <span onClick="deleteCategory(\''+category_row[0]+'\',\''+topic_id+'\',\''+thread_id+'\');" class="delete_link" title="Click to delete category"><img src="/media/images/delete-icon.jpeg" width="10px" height="10px"/></span></span>'
                        elif len(data_limit)== 0:
                            if topic_id:
                                active_categories += '<span id="edit_link_span"><a href="/forum/editcategory/'+category_row[0]+'/community/" title="Click to edit category" ><img src="/media/images/edit-icon.jpeg"/></a>  <a href="/'+append_link+'topic/'+ category_row[0] +'/'+ topic_id +'/True"><img src="/media/images/'+append_link+'-icon.png"/></a><span onClick="deleteCategory(\''+category_row[0]+'\',\'forums\',\'\');" class="delete_link" title="Click to delete category"><img src="/media/images/delete-icon.jpeg" width="10px" height="10px"/></span></span>'    
                            else:
                                active_categories += '<span id="edit_link_span"><a href="/forum/editcategory/'+category_row[0]+'/view-all/" title="Click to edit category" ><img src="/media/images/edit-icon.jpeg"/></a>  <a href="/'+append_link+'topic/'+ category_row[0] +'/view-all/True/"><img src="/media/images/'+append_link+'-icon.png"/></a><span onClick="deleteCategory(\''+category_row[0]+'\',\'view\',\'\');" class="delete_link" title="Click to delete category"><img src="/media/images/delete-icon.jpeg" width="10px" height="10px"/></span></span>'   
                active_categories += '</li>'
        elif len(activeCategories) == 0:
            active_categories += '<br/><br/><center><i>No Records Found</i></center><br/><br/><br/>'
        return active_categories
       
register.tag('getCategories', getCategories)
