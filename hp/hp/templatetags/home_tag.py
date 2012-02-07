"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django import template
from django.template import Context
from django.template.loader import get_template
from hp.dbfuncs import get_latest_threads, get_active_categories
from hp.user.models import user as User
from hp.admanager.models import adpool as Adpool
from hp.settings import MEDIA_URL 
from django.http import Http404,HttpResponse
from hp.admanager.models import *
from hp.admanager.views import *
import random
from django.utils.safestring import mark_safe
register = template.Library()
import psycopg2

"""
# @author Mohsin Aijaz, Fouzia Riaz, ...
"""


def getNewestUser(parser, token):
    
    '''
    # This function will responsible for calling NewestUserNode,
    # if tag is propely defined on home page
    '''
    
    try:    
        
        pass
        
    except ValueError:
    
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    
    return NewestUserNode()

class NewestUserNode(template.Node):
    
    '''
    # The Class NewestUserNode will responsible for generating
    # node that will contain display of newest users of healthpark
    # application. When user access page and template tag is loaded
    # it will go the getNewestUser function which instantiate this
    # class and NewestUserNode's render function will return
    # newest user section
    '''
    
    def __init__(self):
        pass
    
    def render(self, context):
        
        '''
        # Return 12 Newest Users of HealthPark Application
        '''
        
        newestuser = ""
        
        try:
            
            # Getting 12 Newest Users
            totalusers = User.objects.order_by("-join_date_time")[0:12]
            
            # Generating design for User
            for var in totalusers:
                
                newestuser += '''<li>
                        <div class="user_img"><a href="javascript:void(0)">
                        <img src="''' + MEDIA_URL + '''images/media/img_user.gif"
                        alt=""></a></div>
                        <div class="user_name">''' + var.nickname[0:5] + '''</div></li>'''
        
        except:
            
            return newestuser
        
        return newestuser
  
register.tag('getNewestUser', getNewestUser)

def getSponseredLinks(parser, token):
    
    '''
    # This function will responsible for calling NewestUserNode,
    # if tag is propely defined on home page
    '''
    
    try:    
        pass
        
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    
    return Sponseredlinksnode(token.split_contents()[1])

class Sponseredlinksnode(template.Node):
    
    '''
    # The Class Sponseredlinksnode will responsible for generating
    # node that will display ads. When user load page and template 
    # tag is loaded, the render function of Sponseredlinksnode
    # will access DB and search ads for current url in ad-pool,
    # than from the numerous ads random.choice function will 
    # return random ads from list extracted from DB
    '''
    
    def __init__(self, adType):
        
        self.adType = adType
                
    
    def render(self, context):
        
        '''
        # Return random ads from list of ads matching current url
        '''
        
        targetpage = str(context['request'].path)
       
        adshtml = ""
        
        try:
            
            checkAdPool(str(self.adType))
            
            # Getting ads whose for current display type that has not been displayed
            ads = Adpool.objects.filter(adtype=str(self.adType), isdisplayed = False)
            
            myTargetPageList = Adpool.objects.none()
           
            # Getting ads whose targetpages matched with current url
            for eachAd in ads:
                
                # Getting target pages of ad in loop
                targetpageslist = eachAd.targetpages.split(',')
                
                # Matching current url in target pages
                for eachTargetPage in targetpageslist:
                    
                    if str(targetpage) == str(eachTargetPage):
                    
                        myTargetPageList = myTargetPageList | Adpool.objects.filter(id = eachAd.id)
                        
            # Selecting random ad from matched ads if targetpages are matched
            
            if myTargetPageList:
            
                adToDisplay = random.choice(myTargetPageList)
                        
                adshtml += '''<div>''' + adToDisplay.ad + '''</div>'''
                
                adToDisplay.isdisplayed = True
                
                adToDisplay.save()
        
        except:
        
            return adshtml
        
        return adshtml
  
register.tag('getSponseredLinks', getSponseredLinks)


def getLatestForumContent(parser, token):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function for Latest Forum Content Displayed on Home Page
    """
    
    try:    
        pass   

    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return LatestForumContent(token.split_contents()[1],token.split_contents()[2],token.split_contents()[3])


class LatestForumContent(template.Node):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Class For Latest Forum Content Displayed on Home Page 
    """
    
    def __init__(self, view_from_page, is_userLogged, owner):
        self.view_from_page = template.Variable(view_from_page)
        self.is_userLogged = template.Variable(is_userLogged)
        self.owner = template.Variable(owner)
    
    def render(self, context):
        view_from_page = self.view_from_page.resolve(context)
        is_userLogged = self.is_userLogged.resolve(context)
        owner = self.owner.resolve(context)
        forumCount = ""
        if view_from_page == 'home':
            forumContent = get_latest_threads("mostpopular", "limit 4")
        elif  view_from_page == 'medical-content':
            forumContent = get_latest_threads("datedtime", "limit 2")        
        latest_forum = '' 
        if len(forumContent) > 0:      
            for forum_row in forumContent:	
                thread_date = forum_row[6]
                thread_time = forum_row[7]
                if forum_row[6] is None or forum_row[6] <= 0:
                    thread_date = '0'  
                if forum_row[7] is None or forum_row[7] <= 0:
                    thread_time = '0'                
                if forum_row[5] > 0:
                    thread_count = forum_row[5]-1
                elif forum_row[5] == 0:
                    thread_count = forum_row[5] 
                if view_from_page == 'medical-content':
                    thread_body = forum_row[2][0:60]+"...."
                elif view_from_page == 'home':   
                    thread_body = forum_row[2]
                if owner == forum_row[11]:
                    display_activity_links = 'true'
                elif owner != forum_row[11]:
                    display_activity_links = 'false'
                if forum_row[12]:
                    is_locked = True
                else:
                    is_locked = False    
                                         
                forum_context = {'id':forum_row[0],
                                 'thread_count':thread_count,
                                 'thread_date':thread_date,
                                 'thread_time':thread_time,
                                 'first_name':forum_row[3],
                                 'last_name':forum_row[4],
                                 'thread_topic':forum_row[1],
                                 'thread_body':mark_safe(thread_body),
                                 'topic_id':forum_row[10],
                                 'view_from_page':view_from_page,
                                 'most_popular':forum_row[8],
                                 'user_isLogged':is_userLogged,
                                 'display_activity_links':display_activity_links,
                                 'is_locked':is_locked}    
                forum_template = get_template('home_forumContent.html')
                latest_forum += forum_template.render(Context(forum_context))
        elif len(forumContent) == 0:
            latest_forum+= '<br/><br/><center><i>No records found.</i></center></br/></br/>'        
        return latest_forum

  
register.tag('getLatestForumContent', getLatestForumContent)


def getActiveCategories(parser, token):
    
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Active Categories Displayed on Home Page
    """
    
    try:    
        pass

    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return ActiveCategories(token.split_contents()[1],token.split_contents()[2])


class ActiveCategories(template.Node):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Class for Active Categories Displayed on Home Page
    """ 
    
    def __init__(self, user_isLogged, user_id):
        self.user_isLogged = template.Variable(user_isLogged)
        self.user_id   = template.Variable(user_id)
    
    def render(self, context):
        user_isLogged = self.user_isLogged.resolve(context)
        user_id       = self.user_id.resolve(context) 
        
        activeCategories = get_active_categories('limit 7')
        active_categories = ''
        if len(activeCategories) > 0:
            for category_row in activeCategories:	
                if len(category_row[1]) > 10:
                    category_title = category_row[1][0:15]+'...'
                else:
                    category_title = category_row[1]
                active_categories += '<li>'
                active_categories += '<a href="/forum/?cat_id='+category_row[0]+'/" class="ac_cat_list" title="'+category_row[1]+'" >'+category_title+'</a>'
                if user_isLogged:
                    if category_row[4] == user_id:
                        if category_row[7]:
                            append_link = 'unlock'
                        else:
                            append_link = 'lock'
                        #active_categories += '<span id="edit_link_span"><a href="/forum/editcategory/'+category_row[0]+'/"><img src="../media/images/edit-icon.jpeg"/></a>  <a href="/'+append_link+'topic/'+ category_row[0] +'"><img src="../media/images/'+append_link+'-icon.png"/></a>  <a href="/forum/deletecategory/'+category_row[0]+'/"><img src="../media/images/delete-icon.jpeg" width="10px" height="10px"/></a></span>'
                        active_categories += '<span id="edit_link_span"><a href="/forum/editcategory/'+category_row[0]+'/" title="Click to edit category" ><img src="../media/images/edit-icon.jpeg"/></a>  <a href="/'+append_link+'topic/'+ category_row[0] +'" ><img src="../media/images/'+append_link+'-icon.png"/></a>  <span onClick="deleteActiveCategory(\''+category_row[0]+'\');" class="delete_link" title="Click to delete category"><img src="../media/images/delete-icon.jpeg" width="10px" height="10px"/></span></span>'
                active_categories += '</li>'
        elif len(activeCategories) == 0:
            active_categories += '<br/><br/><center><i>No records found.</i></center></br/></br/>'        
        return active_categories
  
register.tag('getActiveCategories', getActiveCategories)

