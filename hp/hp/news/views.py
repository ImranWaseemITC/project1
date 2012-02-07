from django.template import RequestContext

from django.shortcuts import render_to_response
from hp.hp_utils import is_userLogged
from hp.forum.forms import new_thread_form

def display_feeds(request, news_id=None):
    userstatus = is_userLogged(request)
    reply_form = new_thread_form()
    if news_id:
            return render_to_response('news_item.html', 
                                      {'user_isLogged':userstatus,
                                       'reply_form':reply_form,
                                       'news_id':news_id}, context_instance=RequestContext(request))
            
    return render_to_response('horizontal_summarized_all.html', context_instance=RequestContext(request))






