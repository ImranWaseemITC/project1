import datetime,uuid

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response

from django.template import Context

from django.template.loader import get_template

from django.shortcuts import RequestContext,HttpResponse

from django.db.models import Q

from django.utils.safestring import mark_safe

from hp.forum.forms import new_thread_form, search_form, edit_category_form,edit_thread_form

#from hp.forum.models import topic, thread as Thread, thread_group as Thread_Group, topic_group as Topic_Group

from hp.dbfuncs import get_topic_threads, get_latest_threads, get_threads_by_id, add_new_category, get_tree_by_id

from hp.forum.models import thread as Thread, topic as Topic

from hp.user.models import user as User

from hp.hp_utils import is_userLogged,isUserAction

from hp.models import hptb_attachments  # Model for file uploads By Anwar


def newThread(request, news_id=None, topic_id=None, parent_id=None, is_parent=None, origthread_id=None):
    '''
     Inserts a new thread to the database with given relations.
    '''
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

    try:
        user_status = is_userLogged(request)
        if (Topic.objects.get(id = topic_id)).is_locked:
            redirect_url=r'/forum/?cat_id=%s/' % topic_id
            return HttpResponseRedirect(redirect_url)
        else:
            try:
                # Check if a user is logged in. Otherwise redirect to login page.
                logged_user = request.session['User_id']
                
                if request.method == "POST":
                    newThreadForm = new_thread_form(request.POST)
                    if newThreadForm.is_valid():
                        clean_data = newThreadForm.cleaned_data
                        if is_parent and not clean_data['thread_name']:
                            redirect_url=r'/forum/?cat_id=%s/' % topic_id
                            return render_to_response('new_thread.html', 
                                                      {'threadForm': newThreadForm,
                                                       'emptyThreadName':True,'user_isLogged':user_status,'action':action},
                                                       context_instance=RequestContext(request)) 
                    
                        if not clean_data['thread_body']: 
                            return render_to_response('new_thread.html', 
                                                     {'threadForm': newThreadForm,
                                                      'emptyThreadBody':True,'user_isLogged':user_status,'action':action},
                                                      context_instance=RequestContext(request))      
                        
                        try:
                            # Get the user,topic, and thread objects from the database,
                            # for the logged user and given topic and thread ids.
                            owner_user = User.objects.get(id=uuid.UUID(logged_user))
                            #Insert New Category
                            if clean_data['new_category']:
                                new_topic_name = clean_data['new_category']
                                category = add_new_category(new_topic_name, owner_user)
                                categ_topic = Topic.objects.get(id=str(category))    
                            else:  
                                if clean_data['category_id']: 
                                    categ_topic = Topic.objects.get(id=topic_id)
                                else:
                                    return render_to_response('new_thread.html', 
                                                              {'threadForm': newThreadForm,
                                                               'emptyCategory':True,'user_isLogged':user_status,'action':action},
                                                              context_instance=RequestContext(request))   
                                
                            parentThread = Thread.objects.get(id=parent_id)
                        except User.DoesNotExist:
                            pass
                        except Topic.DoesNotExist:
                            pass
                        except Thread.DoesNotExist:
                            # If no parent_id was passed to the view,
                            # set parentThread to None. 
                            parentThread=None
                        
                        # Create a new uuid.
                        new_thread_id = uuid.uuid4()
                        
                                
                        # Create a new thread instance to save to the db.
                        new_thread = Thread(id = new_thread_id,
                                            thread_name = clean_data['thread_name'],
                                            thread_body = clean_data['thread_body'],
                                            datetime_created = datetime.datetime.now(),
                                            keyword_dict = clean_data['keywords'],
                                            topic = categ_topic,
                                            owner = owner_user,
                                            parent_thread = parentThread,
                                            most_popular = 0,
                                            )
                        
                        try:
                            new_thread.save()
                            allowed_content_list=['application/pdf', 'application/zip','image/gif', 'image/jpeg','image/pjpeg']
                            
                            try:
                                docfile1=request.FILES['docfile']
                                c_type=docfile1.content_type
                                if 'docfile' in request.FILES and c_type in allowed_content_list:
                                    newdoc = hptb_attachments(hptable_ID='th',hprecord_id=new_thread_id, docfile = request.FILES['docfile'], )
                                    newdoc.save()
                            except:
                                pass        
                            # If the thread to be saved is a top-level parent thread,
                            # redirect to the new parent thread created. Otherwise
                            # redirect to the same thread page where user was last.
                            if is_parent:
                                id_list = (topic_id, new_thread_id)
                            else:
                                id_list=(topic_id, origthread_id)
                            request.session['Action'] = 'add-post'    
                            redirect_url=r'/forum/?topic_id=%s&thread_id=%s/' % id_list
                            return HttpResponseRedirect(redirect_url)
                            
                        except:
                            return render_to_response('new_thread.html', 
                                                      {'threadForm': newThreadForm, 'dberror':True,'user_isLogged':user_status,'action':action},
                                                      context_instance=RequestContext(request))
                        
            except KeyError:
                return HttpResponseRedirect('/login/')
            
        
        categ_topic = Topic.objects.get(id=topic_id)
        threadForm = new_thread_form(initial = {'category_id':categ_topic})
        return render_to_response('new_thread.html', {'threadForm': threadForm,'user_isLogged':user_status,'category_name':categ_topic.topic_name,'cat_id':topic_id,'action':action},
                                  context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect('/')    
            
    
def threadVote(request, thread_id, topic_id, origthread_id,  up=None, down=None, view_all=None):
    '''
     For the given thread_id increases or decreases the votes
     for that thread, depending on parameters
    '''

    if is_userLogged(request):
        try:
            # Fetch the thread from database that matches given thread id.
            vote_thread = Thread.objects.get(id=thread_id)
        except:
            pass
        if up:
            # If up parameter recieved, add one to popularity field
            vote_thread.most_popular = vote_thread.most_popular + 1
        if down:
            # If down parameter recieved, subtract one from popularity field
            vote_thread.most_popular = vote_thread.most_popular - 1
        
        try:
            vote_thread.save()
        except:
            pass
        if origthread_id:
            redirect_url = '/forum/?topic_id='+topic_id+'&thread_id='+origthread_id
        elif topic_id:
            if view_all:
                redirect_url = '/forum/view-all/'    
            else:    
                redirect_url = '/forum/?cat_id='+topic_id
        else:
            redirect_url = '/'  
            #redirects_url = '/refresh_page/'    
        return HttpResponseRedirect(redirect_url)
    redirect_path=request.get_full_path()
    return HttpResponseRedirect('/login/?next='+redirect_path)
    
def displayTopic(request, topic_id=None, parent_id=None):
    is_locked = '';category_name = '';thread_name = ''
    if request.method == "POST":
        reply_form = new_thread_form(request.POST)
        if reply_form.is_valid():
            clean_data = reply_form.cleaned_data
            logged_user = request.session['User_id']

            try:
                owner_user = User.objects.get(id=uuid.UUID(logged_user))
                parentThread = Thread.objects.get(id=parent_id)
                categ_topic = Topic.objects.get(id=topic_id)
            except:
                return HttpResponseRedirect('/')   
            new_thread = Thread(thread_name = clean_data['thread_name'],
                                thread_body = clean_data['thread_body'],
                                datetime_created = datetime.datetime.now(),
                                keyword_dict = clean_data['keywords'],
                                topic = categ_topic,
                                owner = owner_user,
                                parent_thread = parentThread,
                                most_popular = 0,
                                )
                
            try:
                new_thread.save()
                id_list=(topic_id, parent_id)
                redirect_url=r'/forum/?topic_id=%s&thread_id=%s/' % id_list
                return HttpResponseRedirect(redirect_url)
            except:
                pass
            
    
    try:
        
        thread_id = '';cat_id = '';display_forum = 0;display_thread = 0;threadsList = [];topic_id='' 
        if request.GET.get("cat_id"):
            cat_id = str(request.GET.get("cat_id"))
            cat_id = cat_id.rstrip('/')
            categories = ""
        if request.GET.get("topic_id"):
            topic_id = str(request.GET.get("topic_id"))
            topic_id = topic_id.rstrip('/')
            try:
                category_content = Topic.objects.get(id=topic_id)
                category_name = category_content.topic_name
            except:
                pass#return HttpResponseRedirect('/')    
            categories = ""    

        if request.GET.get("thread_id"):
            thread_id = str(request.GET.get("thread_id"))
            thread_id = thread_id.rstrip('/')
            try:
                parentThread = Thread.objects.get(id=thread_id)
                thread_name = parentThread.thread_name
            except:
                pass
            categories = ""
    except ValueError:
        pass
    # if (not thread_id or thread_id == '' or len(thread_id) == 0):
    #     thread_id = None   
    #     threadsList = get_threads_by_id(thread_id)
    # else:
    #     threadsList = get_threads_by_id(thread_id)
    if not thread_id and not cat_id:
        categories = 'TRUE'
        is_locked = ''       
    if request.GET.get("cat_id"):
        display_forum = 'TRUE'
        try:
            category_content = Topic.objects.get(id = cat_id)
        except:
            return HttpResponseRedirect('/')    
        is_locked = category_content.is_locked
        category_name = category_content.topic_name
    if request.GET.get("thread_id"):
        parent_id = request.GET.get("thread_id")
        parent_id = parent_id.rstrip('/')
        try:
            parentThread = Thread.objects.get(id=parent_id)
            thread_name = parentThread.thread_name
        except:
            pass
        #    return HttpResponseRedirect('/')     
        display_thread = 'TRUE'
        is_locked = ''
        
    user_status = is_userLogged(request);
    if user_status: 
        logged_user = request.session['User_id']
    else: 
        logged_user = '' 
    
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
    reply_form = new_thread_form()
    template_search_form = search_form()
    return render_to_response('forum_page.html', {#'threads':threadsList,
                                                  'display_forum':display_forum,
                                                  'display_thread':display_thread,
                                                  'category':cat_id,
                                                  'thread':thread_id,
                                                  'topic_id':topic_id,
                                                  'display_category':categories,
                                                  'path':request.get_full_path(),
                                                  'user_isLogged':user_status,
                                                  'reply_form':reply_form,
                                                  'search_form':template_search_form,
                                                  'owner':logged_user,
                                                  'topic_is_locked':is_locked,
                                                  'action':action,
                                                  'category_name':category_name,
                                                  'thread_name':thread_name},
                                                  context_instance=RequestContext(request))

def getForumContext(forum_row, is_topic, topic_count,is_userLogged,owner,view_page):
    
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Forum Activity Context Required In ForumActivity Class 
    """ 
    
    if is_topic == 'true':
        thread_date = forum_row[9]
        thread_time = forum_row[10]
        most_popular = forum_row[7]
        if forum_row[9] is None or forum_row[9] <= 0:
            thread_date = '0'  
        if forum_row[10] is None or forum_row[10] <= 0:
            thread_time = '0'                
        if forum_row[8] > 0:
            thread_count = forum_row[8] - 1
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
            thread_count = forum_row[5] - 1
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
    forum_context = {'id':forum_row[0],
                     'thread_count':thread_count,
                     'thread_date':thread_date,
                     'thread_time':thread_time,
                     'first_name':forum_row[3],
                     'last_name':forum_row[4],
                     'thread_topic':forum_row[1],
                     'thread_body':mark_safe(forum_row[2]),
                     'topic_count':topic_count,
                     'most_popular':most_popular,
                     'topic_id':forum_row[11],
                     'user_isLogged':is_userLogged,
                     'display_activity_links':display_activity_links,
                     'view_page':view_page,
                     'is_locked':is_locked}
    
    return forum_context

def orderMoreForumActivity(request, offset): 
    
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Latest Forum Content Order BY/See more on Forum Page 
    """ 
    user_status = is_userLogged(request)
    if user_status:
        logged_user = request.session['User_id']
    else:
        logged_user = ''    
    

    order_field = "mostpopular";
    try:    
            #If parameters send in url (LIMITS, COUNTS, ORDERS, Category) (For See more, category)
            if (request.GET.get("lim") and request.GET.get("off") and request.GET.get("counts")) or request.GET.get("orders") or (request.GET.get("cat_id")) :
                content_limit = str(request.GET.get("lim")).rstrip('/')
                content_offset = str(request.GET.get("off")).rstrip('/')
                content_count = str(request.GET.get("counts")).rstrip('/')
                order_field = str(request.GET.get("orders")).rstrip('/')
                catid_field = str(request.GET.get("cat_id")).rstrip('/')
                catid_field = catid_field.rstrip('/')
                order_field = order_field.rstrip('/')
            
    except ValueError:
        pass     
    if order_field !="":
        #If no limits provided in url
        if content_limit == 'None'or content_limit is None:
            if catid_field is None or catid_field == 'None':
                catid_field = "null"
            forumContent = get_topic_threads(catid_field, order_field, "limit 5")
        
        #If limits provided in url
        else: 
            limits = "limit "+content_limit+" offset "+content_offset   
            forumContent = get_topic_threads(catid_field, order_field, limits)  
        forumActivityCount = get_topic_threads(catid_field, "mostpopular", "")
        topic_count = len(forumActivityCount)
        is_topic = 'true';forum_activity = ''
        if catid_field == "null":
            view_page = 'view-all-forum'
        else:
            view_page = ''    
        if len(forumContent) > 0:
            for forum_row in forumContent:    
                
                if is_topic == 'true':
                    forum_context = getForumContext(forum_row, is_topic, topic_count, user_status,logged_user,view_page)
                else:
                    forum_context = getForumContext(forum_row, is_topic, topic_count, user_status,logged_user,view_page)
    
                forum_template = get_template('home_forumContent.html')
                forum_activity += forum_template.render(Context(forum_context))
        elif len(forumContent) == 0:
            forum_activity += '<br/><br/><center><i>No records found.</i></center></br/></br/>'  
        if len(catid_field) != 0:
            forum_activity += '<input type="hidden" value="'+catid_field+'" id="cat_id"/>' 
        forum_activity += '<input type="hidden" value="'+`topic_count`+'" id="topic_count"/><input type="hidden" value="'+order_field+'" id="order_by"/>'                                    
        return HttpResponse(forum_activity)

def orderForumActivityHome(request, offset): 
    
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Latest Forum Content Order BY Display on Home Page (AJAX)
    """ 
    user_status = is_userLogged(request)
    if user_status:
        logged_user = request.session['User_id']
    else:
        logged_user = ''    
    try:
        order_field = str(offset)
    except ValueError:
        pass     
    forumContent = get_latest_threads(order_field, "limit 4")
    user_status = is_userLogged(request)
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
                thread_count = forum_row[5] - 1
            elif forum_row[5] == 0:
                thread_count = forum_row[5]             
            if logged_user == forum_row[11]:
                display_activity_links = 'true'
            elif logged_user != forum_row[11]:
                display_activity_links = 'false'  
            if forum_row[12]:
                is_locked = True
            else:
                is_locked = False    
            forum_context = {'id':forum_row[0],'thread_count':thread_count,'thread_date':thread_date,'thread_time':thread_time,'first_name':forum_row[3],'last_name':forum_row[4],'thread_topic':forum_row[1],'thread_body':mark_safe(forum_row[2]),'topic_id':forum_row[10],'most_popular':forum_row[8],'user_isLogged':user_status,'display_activity_links':display_activity_links,'is_locked':is_locked,'view_from_page':'home'}    
            forum_template = get_template('home_forumContent.html')
            latest_forum += forum_template.render(Context(forum_context)) 
    elif len(forumContent) == 0: 
        latest_forum += '<br/><br/><center><i>No records found.</i></center></br/></br/>'     
    return HttpResponse(latest_forum)

def forumContentByTopic(request, offset): 
    
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Latest Forum Content Order BY Display on Forum Page
    """ 
    
    user_status = is_userLogged(request)
    if user_status:
        logged_user = request.session['User_id']
    else:
        logged_user = ''    
    try:
        topic_id = offset
    except ValueError:
        pass   
  
    try:
        topic_id = offset
    except ValueError:
        pass 
    try:    
        getCategory = Topic.objects.get(id=topic_id)
        if getCategory.id:
            forumContent = get_topic_threads(topic_id)
            latest_forum_by_topic = ''
            if len(forumContent) > 0:
                for forum_row in forumContent:    
                    thread_date = forum_row[7]
                    thread_time = forum_row[8]
                    #thread_count = forum_row[6]
                    if forum_row[7] is None or forum_row[7] <= 0:
                        thread_date = '0'  
                    if forum_row[8] is None or forum_row[8] <= 0:
                        thread_time = '0'                
                    if forum_row[6] > 0:
                        thread_count = forum_row[6] - 1
                    elif forum_row[6] == 0:
                        thread_count = thread_count 
                    if logged_user == forum_row[11]:
                        display_activity_links = 'true'
                    elif logged_user != forum_row[11]:
                        display_activity_links = 'false'            
                    forum_context = {'id':forum_row[0],'thread_count':thread_count,'thread_date':thread_date,'thread_time':thread_time,'first_name':forum_row[3],'last_name':forum_row[4],'thread_topic':forum_row[1],'thread_body':mark_safe(forum_row[2]),'is_userLogged':user_status,'display_activity_links':display_activity_links}    
                    forum_template = get_template('home_forumContent.html')
                    latest_forum_by_topic += forum_template.render(Context(forum_context))
            elif len(forumContent) == 0: 
                latest_forum_by_topic += '<br/><br/><center><i>No records found.</i></center></br/></br/>'
            return HttpResponse(latest_forum_by_topic)
        else:
            return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')   

def search(request, is_adv=None):
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

    if is_adv:
        return render_to_response('advanced_search.html',
                                  context_instance=RequestContext(request))
    if request.method == "POST":
        searchform = search_form(request.POST)
        if searchform.is_valid():
            clean_data = searchform.cleaned_data
            
            if clean_data['category_choices']:
                # Fend chosen category to template for display
                category_choices = '\'' + str(clean_data['category_choices']) + '\'' + ' category'
                # Retrieve records matching the search query for given category
                try:
                    result_set = Thread.objects.filter(Q(topic=clean_data['category_choices']),
                                                       (Q(thread_name__contains = clean_data["search_text"])|
                                                       Q(thread_body__contains = clean_data["search_text"])),
                                                       Q(parent_thread = None))
                except:
                    pass
            else:
                category_choices = 'all forums'
                try:
                    result_set = Thread.objects.filter(Q(thread_name__contains = clean_data["search_text"])|
                                                       Q(thread_body__contains = clean_data["search_text"]),
                                                       Q(parent_thread = None))
                except:
                    pass
                
            result_set_count = len(list(result_set))
            user_status = is_userLogged(request)
            return render_to_response('search.html',
                                      {'threads':result_set, 
                                       'threads_count':result_set_count, 
                                       'search_text':clean_data["search_text"],
                                       'category_choices': category_choices,
                                       'search_form':searchform,
                                       'user_isLogged':user_status,'action':action},
                                       context_instance=RequestContext(request))
        return render_to_response('search.html', {'search_form':searchform})
    return HttpResponseRedirect('/forum/')

def editCategory(request, category_id=None, topic_id=None, thread_id=None):  
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Change Category
    """
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

    try:
        # Check if a user is logged in. Otherwise redirect to login page.
        logged_user = request.session['User_id']
        user_status = is_userLogged(request)
        if request.method == "POST":
            editTopicForm = edit_category_form(request.POST)
            if editTopicForm.is_valid():
                clean_data = editTopicForm.cleaned_data  
                owner_user = User.objects.get(id=uuid.UUID(logged_user))  
                try:
                    #owner_user = User.objects.get(id=uuid.UUID(logged_user))
                    if len(clean_data['category_name']) == 0:
                        return render_to_response('edit_category.html', 
                                                      {'editTopicForm': editTopicForm,
                                                       'emptyCategory':True,'user_isLogged':user_status,'action':action},
                                                                  context_instance=RequestContext(request)) 
                    else:
                        editCategory = Topic.objects.get(id=category_id)
                        editCategory.topic_name=clean_data['category_name']
                        editCategory.topic_body=topic_body=clean_data['category_body']
                        editCategory.keyword_dict=keyword_dict=clean_data['category_keywords']            
                        try:
                            if editCategory.owner == owner_user:
                                editCategory.save()
                                if not topic_id is None and not thread_id is None:
                                    id_list = (topic_id, thread_id)
                                    redirect_url=r'/forum/?topic_id=%s&thread_id=%s/' % id_list
                                elif not topic_id is None and thread_id is None:
                                    if topic_id == 'community':
                                        redirect_url=r'/forum/' 
                                    elif topic_id == 'view-all':
                                        redirect_url=r'/forum/view-all/' 
                                    else:       
                                        redirect_url=r'/forum/?cat_id=%s' % (topic_id)
                                elif topic_id is None and thread_id is None:  
                                    redirect_url=r'/'
                                request.session['Action'] = 'edit-category'      
                                return HttpResponseRedirect(redirect_url)
                        except:
                            return render_to_response('edit_category.html', 
                                                      {'editTopicForm': editTopicForm, 'dberror':True,'user_isLogged':user_status,'action':action},
                                                      context_instance=RequestContext(request))
                except:
                    return HttpResponseRedirect('/')                               
        #except KeyError:
        #    return HttpResponseRedirect('/login/')*/
        
        #Select Values From Database
        category_content = Topic.objects.get(id = category_id)
        editTopicForm = edit_category_form(initial = {'category_name':category_content.topic_name,
                                                      'category_body':category_content.topic_body,
                                                      'category_keywords':category_content.keyword_dict})
        return render_to_response('edit_category.html', {'editTopicForm': editTopicForm,'user_isLogged':user_status,'category_name':category_content.topic_name,'action':action},
                                  context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect('/')       

def locker(request, object_id, lock, object_type, disptopic_id=None, return_to_forum=None):
    try:
        if object_type == 'topic':
            lock_object = Topic.objects.get(id=object_id)
        elif object_type == 'thread':
            lock_object = Thread.objects.get(id=object_id)
            
        if request.session['User_id'] == lock_object.owner.id:
            lock_object.is_locked = lock
            lock_object.save()
            
        if disptopic_id and object_type == 'thread':
            redirect_url = '/forum/?topic_id='+disptopic_id+'&thread_id='+object_id
        elif disptopic_id:
            if disptopic_id == "view-all":
                redirect_url = '/forum/view-all/'
            else:    
                redirect_url = '/forum/?cat_id='+disptopic_id
        elif return_to_forum:
                redirect_url = '/forum/'
        else:
            redirect_url = '/'
        request.session['Action'] = ''   
        if lock == True: 
            if object_type == 'topic':
                request.session['Action'] = 'lock-category' 
            elif object_type == 'thread':
                request.session['Action'] = 'lock-post'      
        elif lock == False: 
            if object_type == 'topic':
                request.session['Action'] = 'unlock-category'
            elif object_type == 'thread':
                request.session['Action'] = 'unlock-post'             
        return HttpResponseRedirect(redirect_url)
    except:
        return HttpResponseRedirect('/') 

def editThread(request, thread_id=None, view_page=None, topic_id=None, parent_id=None):
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Edit thread to the database with given relations.
    """
    # Check if a user is logged in. Otherwise redirect to login page.
    user_status = is_userLogged(request)
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

    try:
        logged_user = request.session['User_id']     
        if request.method == "POST":
            editThreadForm = edit_thread_form(request.POST)
            if editThreadForm.is_valid():
                clean_data = editThreadForm.cleaned_data
                owner_user = User.objects.get(id=uuid.UUID(logged_user))  
                if not clean_data['thread_name']: 
                    return render_to_response('new_thread.html', 
                                              {'threadForm': editThreadForm,
                                               'emptyThreadName':True,'actions':'edit','user_isLogged':user_status,'action':action},
                                              context_instance=RequestContext(request))
                    
                if not clean_data['thread_body']: 
                    return render_to_response('new_thread.html', 
                                              {'threadForm': editThreadForm,
                                              'emptyThreadBody':True,'actions':'edit','user_isLogged':user_status,'action':action},
                                              context_instance=RequestContext(request))      
                    
                       
            # Edit thread instance to save to the db.
                try:
                    edit_thread = Thread.objects.get(id = thread_id)
                    edit_thread.thread_name      = clean_data['thread_name']
                    edit_thread.thread_body      = clean_data['thread_body']
                    edit_thread.keyword_dict     = clean_data['keywords']
                    #edit_thread.topic           = clean_data['category_id']
                except:
                    return HttpResponseRedirect('/')     
                
                try:
                    if edit_thread.owner == owner_user:
                        edit_thread.save()
                        try:
                            allowed_content_list=['application/pdf', 'application/zip','image/gif', 'image/jpeg','image/pjpeg']
                            docfile1=request.FILES['docfile']
                            c_type=docfile1.content_type
                            if 'docfile' in request.FILES and c_type in allowed_content_list:
                                newdoc = hptb_attachments(hptable_ID='th',hprecord_id=thread_id, docfile = request.FILES['docfile'], )
                                newdoc.save()
                        except:
                            pass        
                    if view_page == 'home':
                        redirect_url ='/'
                    if view_page == 'forum':
                        redirect_url=r'/forum/?cat_id=%s/' % (topic_id)
                    if view_page == 'thread':    
                        redirect_url=r'/forum/?topic_id=%s&thread_id=%s/' % (topic_id, parent_id)
                    if view_page == 'view-all':
                        redirect_url ='/forum/view-all/'    
                    request.session['Action'] = 'edit-post' 
                    return HttpResponseRedirect(redirect_url)
                
                except:
                    return render_to_response('new_thread.html', 
                                          {'threadFrom': editThreadForm, 'dberror':True,'actions':'edit','user_isLogged':user_status,'action':action},
                                          context_instance=RequestContext(request))                    
    except KeyError:
        return HttpResponseRedirect('/login/')
    #Select Values From Database
    try:
        thread_content = Thread.objects.get(id = thread_id)
        category_content = Topic.objects.get(id = topic_id)
        threadForm = edit_thread_form(initial = {#'category_id':category_content,
                                                 'thread_name':thread_content.thread_name,
                                                 'thread_body':thread_content.thread_body,
                                                 'keywords':thread_content.keyword_dict})
        return render_to_response('new_thread.html', {'threadForm': threadForm,'actions':'edit','user_isLogged':user_status,'category_name':category_content.topic_name,'cat_id':category_content.id,'action':action},context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect('/')              

def deleteCategory(request, category_id=None, topic_id=None, thread_id=None):  
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Delete Category
    """
    try:
        # Check if a user is logged in. Otherwise redirect to login page.
        logged_user = request.session['User_id']
        owner_user = User.objects.get(id=uuid.UUID(logged_user)) 
        try:
            deleteCategory = Topic.objects.get(id=category_id)   
            if deleteCategory.owner == owner_user:
                deleteCategory.delete()
                deleteCategory.objects.all()
            
        except:
            pass  
        if not topic_id is None and not thread_id is None:
            id_list = (topic_id, thread_id)
            redirect_url=r'/forum/?topic_id=%s&thread_id=%s/' % id_list
        elif (not topic_id is None) and (thread_id is None) and topic_id != category_id:
            if topic_id == "forums":
                redirect_url=r'/forum/'
            elif topic_id == "view-all":
                redirect_url=r'/forum/view-all/'
            else:
                redirect_url=r'/forum/?cat_id=%s' % (topic_id)
        elif (not topic_id is None) and (thread_id is None) and topic_id == category_id:
            redirect_url=r'/'
        elif topic_id is None and thread_id is None:  
            redirect_url=r'/'  
        request.session['Action'] = 'del-category' 
        return HttpResponseRedirect(redirect_url)
    except KeyError:
        return HttpResponseRedirect('/login/') 

def deleteThread(request, thread_id=None, view_page=None, topic_id=None, parent_id=None):  
    """
    @AUTHOR:Fouzia Riaz
    @DESCRIPTION:Function For Delete Post/Response
    """
    try:
        # Check if a user is logged in. Otherwise redirect to login page.
        logged_user = request.session['User_id']
        owner_user = User.objects.get(id=uuid.UUID(logged_user)) 
        threadsList = get_tree_by_id(thread_id) 
        for thread_row in threadsList:
            try:
                delete_thread = Thread.objects.get(id = thread_row[0])
                if thread_row[13] == logged_user:
                    delete_thread.delete()
                    delete_thread.objects.all()
                
            except:
                pass
        if view_page == 'home':
            redirect_url ='/'
        elif view_page == 'forum':
            redirect_url=r'/forum/?cat_id=%s/' % (topic_id)
        elif view_page == 'thread':    
            redirect_url=r'/forum/?topic_id=%s&thread_id=%s/' % (topic_id, parent_id)
        elif view_page == 'view-all':    
            redirect_url=r'/forum/view-all/'   
        else:
            redirect_url = '/'
        request.session['Action'] = 'del-post'     
        return HttpResponseRedirect(redirect_url)
    except KeyError:
        return HttpResponseRedirect('/login/') 

def displayAllThreads(request, view_all=None):
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
    return render_to_response('forum_thread_page.html', {'user_isLogged':user_status, 'owner':user_id,'action':action,
                                                  },
                                                  context_instance=RequestContext(request))    

  

