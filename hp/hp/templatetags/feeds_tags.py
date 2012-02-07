"""
Tags which can retrieve and parse RSS and Atom feeds, and return the
results for use in templates.

Based, in part, on the original idea by user baumer1122 and posted to
djangosnippets at http://www.djangosnippets.org/snippets/311/

"""

import feedparser, uuid

from datetime import datetime, timedelta

from dateutil.parser import parse

from django import template

from django.template.loader import render_to_string

from hp.dbfuncs import update_news_model

from hp.news.models import newsItem


register = template.Library()

class ContextUpdatingNode(template.Node):
    """
    Node that updates the context with certain values.
    
    Subclasses should define ``get_content()``, which should return a
    dictionary to be added to the context.
    
    """
    def render(self, context):
        context.update(self.get_content(context))
        return ''

    def get_content(self, context):
        raise NotImplementedError
    
class FeedIncludeNode(template.Node):
    def __init__(self, feed_url, template_name, num_items=None):
        self.feed_url = template.Variable(feed_url)
        self.num_items = num_items
        self.template_name = template_name

    def render(self, context):
        feed_url = self.feed_url.resolve(context)
        feed = feedparser.parse(feed_url)
        items = []
        num_items = int(self.num_items) or len(feed['entries'])
        for i in range(num_items):
            pub_date = feed['entries'][i].updated_parsed
            published = datetime.date(pub_date[0], pub_date[1], pub_date[2])
            items.append({ 'title': feed['entries'][i].title,
                           'summary': feed['entries'][i].summary,
                           'link': feed['entries'][i].link,
                           'date': published })
        return render_to_string(self.template_name, { 'items': items,
                                                      'feed': feed })


class FeedParserNode(ContextUpdatingNode):
    def __init__(self, varname, param):
        self.varname = varname
        self.param = template.Variable(param)
        pass
    
    def get_content(self, context):
        param = self.param.resolve(context)
        
        # Get the date of the last news database update.
        update_news = newsItem.objects.get(id=uuid.UUID('c2c66fdb-b569-452f-b521-3ccefe5bc095'),
                                           title='last_updated',
                                           summary='last_updated',
                                           body='last_updated',
                                           author='last_updated')
        
        # If last update date is older than current date,
        # update database with latest news.
        if (parse(datetime.now().ctime())-parse(update_news.datetime_created.ctime())).total_seconds()/60/60 > 6.0:
            update_news_model("http://reutershealth.mainstreamdata.com/rss/eline.xml")
            update_news.datetime_created = datetime.now()
            update_news.save()
            
        # Fetch news from database, upto 4 days old
        latest_news = newsItem.objects.filter(datetime_created__gt=(datetime.now()-timedelta(days=4)).date()).order_by("-datetime_created").exclude(id=uuid.UUID('c2c66fdb-b569-452f-b521-3ccefe5bc095'))
        
        # If recieved parameter is not an int,
        # then it must be a uuid. Retrieve and 
        # return the details on the news item. 
        if not str(type(param)) == "<type 'int'>":
            try:
                display_news = newsItem.objects.get(id=uuid.UUID(str(param)))
                display_news.last_viewed = datetime.now()
                display_news.save()
                recently_viewed = latest_news.order_by("-last_viewed")
                if len(recently_viewed) > 2:
                    ret_data = {'news_item':display_news, 'recently_viewed':[recently_viewed[1],recently_viewed[2]]}
                elif len(recently_viewed) > 1:
                    ret_data = {'news_item':display_news, 'recently_viewed':[recently_viewed[1],]}
                else:
                    ret_data = {'news_item':display_news}                    
            except:
                pass
            return { self.varname: ret_data }
        
        # Following code executes if recieved parameter is int.
        # Returns param number of latest news items. 
        break_limit = int(param)
        
        ret_entries = []
        for item in latest_news:
            if break_limit == 0:
                break
            break_limit = break_limit-1
            
            # Calculate how long ago the news was created,
            # and divide into days and hours, rounded off.
            time_ago = (datetime.now()-parse(item.datetime_created.ctime())).total_seconds()/60/60/24
            days_ago = int(time_ago)
            if not days_ago==0:
                hours_ago = int(round(time_ago%days_ago*24))
            else:
                hours_ago = int(time_ago*24)
                days_ago=None
                
            ret_entries.append({'id':item.id,
                                'title':item.title, 
                                'summary':item.summary, 
                                'body':item.body,
                                'by':item.author, 
                                'date':item.datetime_created, 
                                'days_ago':days_ago,
                                'hours_ago':hours_ago})
        
        try:
            recently_viewed = latest_news.order_by("-last_viewed")
            if len(recently_viewed) > 1:
                ret_data = {'news_items':ret_entries, 'recently_viewed':[recently_viewed[0],recently_viewed[1]]}
            elif recently_viewed:
                ret_data = {'news_items':ret_entries, 'recently_viewed':[recently_viewed[0],]}
            else:
                ret_data = {'news_items':ret_entries}

        except:
            pass
        return { self.varname: ret_data }

def do_include_feed(parser, token):
    """
    Parse an RSS or Atom feed and render a given number of its items
    into HTML.
    
    It is **highly** recommended that you use `Django's template
    fragment caching`_ to cache the output of this tag for a
    reasonable amount of time (e.g., one hour); polling a feed too
    often is impolite, wastes bandwidth and may lead to the feed
    provider banning your IP address.
    
    .. _Django's template fragment caching: http://www.djangoproject.com/documentation/cache/#template-fragment-caching
    
    Arguments should be:
    
    1. The URL of the feed to parse.
    
    2. The number of items to render (if not supplied, renders all
       items in the feed).
       
    3. The name of a template to use for rendering the results into HTML.
    
    The template used to render the results will receive two variables:
    
    ``items``
        A list of dictionaries representing feed items, each with
        'title', 'summary', 'link' and 'date' members.
    
    ``feed``
        The feed itself, for pulling out arbitrary attributes.
    
    Requires the Universal Feed Parser, which can be obtained at
    http://feedparser.org/. See `its documentation`_ for details of the
    parsed feed object.
    
    .. _its documentation: http://feedparser.org/docs/
    
    Syntax::
    
        {% include_feed [feed_url] [num_items] [template_name] %}
    
    Example::
    
        {% include_feed "http://www2.ljworld.com/rss/headlines/" 10 feed_includes/ljworld_headlines.html %}
    
    """
    bits = token.contents.split()
    if len(bits) == 3:
        return FeedIncludeNode(feed_url=bits[1], template_name=bits[2])
    elif len(bits) == 4:
        return FeedIncludeNode(feed_url=bits[1], num_items=bits[2], template_name=bits[3])
    else:
        raise template.TemplateSyntaxError("'%s' tag takes either two or three arguments" % bits[0])

def do_parse_feed(parser, token):
    """
    Parses the reuters news feed and returns the news items in a given context
    variable.
    
    Arguments should be:
    
    1. The name of a context variable in which to return the result.
    2. Either a number defining the number of summarized news items to return,
       or a the uuid of a news item in database to return details of the news item.
    
    Requires the Universal Feed Parser

    Syntax::
    
        {% parse_feed [varname] [number of items to return/uuid] %}
    
    Example::
    
        {% parse_feed items 100 %}
        or
        {% parse_feed items news_id %}
    
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError(u"'%s' tag takes four arguments" % bits[0])
    return FeedParserNode(bits[1], bits[2])

@register.filter
def truncatesmart(value, limit=80):
    """""""""""""""""""""""""""""""""""""""""""""""""""
    # Truncates a string after a given number of chars #
    # keeping whole words.                             #
    """""""""""""""""""""""""""""""""""""""""""""""""""
    
    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value
    
    # Make sure it's unicode
    value = unicode(value)
    
    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value
    
    try:
        value = value[:value.index('\n')-1]
    except:
        pass
    
    # Cut the string
    value = value[:limit]
    
    # Break into words and remove the last
    words = value.split(' ')[:-1]
    
    # Join the words and return
    return ' '.join(words) + '...'

register.tag('include_feed', do_include_feed)
register.tag('parse_feed', do_parse_feed)
