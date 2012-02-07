"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
import uuid, feedparser, urllib, os

from dateutil.parser import parse

from datetime import datetime

from django.core.files import File

from django.conf import settings

from hp.db import dbConnection

from hp.forum.models import topic

from hp.news.models import newsItem


obj = dbConnection()
connection = obj.connect()


def get_user_topics(username):
    pass

def get_topic_threads(topic, order_field, limits):
    
    """
    # Sql Query For Forum Threads with respect to topic on home page
    """
    
    orderby_field = ''
    if order_field == "datedtime":
        orderby_field = "created"
    elif order_field == "mostpopular": 
        orderby_field = "popular" 
    elif order_field == "mostdiscuss": 
        orderby_field = "count"    
    cursor= connection.cursor()
    tid=str(topic)
    if tid != "null":
        cursor.execute("""Select * from gettree(%s) where parent_id is null order by """+orderby_field+""" desc  """+ limits,[tid])
    else:
        cursor.execute("""Select * from gettree(null) where parent_id is null order by """+orderby_field+""" desc  """+ limits)
    tlist = cursor.fetchall()
    return tlist

def get_threads_by_id(thread_id):
    
    """
    # Sql Query For Forum Threads with/without id
    """
    cursor= connection.cursor()
    tid=thread_id
    query = "Select * from get_thread_tree('"+tid+"');"
    cursor.execute(query)
    
    tlist = cursor.fetchall()
    return tlist

def get_tree_by_id(thread_id):
    
    """
    # Sql Query For Forum Threads with/without id
    """
    cursor= connection.cursor()
    tid=thread_id
    query = "Select * from get_thread_tree_by_id('"+tid+"');"
    cursor.execute(query)
    
    tlist = cursor.fetchall()
    return tlist

def get_latest_threads(order_field, limits):

    """
    # Sql Query For Latest Forum Content Order BY Display on Home Page 
    """
    orderby_field = ''
    if order_field == "datedtime":
        orderby_field = "dateTimeCreated"
    elif order_field == "mostpopular": 
        orderby_field = "mostpopular" 
    elif order_field == "mostdiscuss": 
        orderby_field = "count"        
    cursor= connection.cursor()   
    cursor.execute("""select * from get_latest_parent_threads() order by """ + orderby_field+""" desc """ + limits)
    tlist = cursor.fetchall()
    return tlist

def get_active_categories(limits):
    
    """
    # Sql Query For Active Categories Displayed on Home Page
    """
    
    cursor= connection.cursor()
    cursor.execute("select * from forum_topic order by \"topic_name\" asc " +limits)
    tlist = cursor.fetchall()
    return tlist

def add_new_category(category_name,owner_id):
    """
    # Sql Query For Select Categories By Name
    """
    cursor= connection.cursor()
    cursor.execute("select * from forum_topic where \"topic_name\" = '"+category_name+"'")
    tlist = cursor.fetchall()
    if len(tlist) == 0:
        new_cat_id = uuid.uuid4()
        addTopic = topic(id = new_cat_id,
                         topic_name = category_name,
                         topic_body = '',
                         moderator = owner_id,
                         owner = owner_id)
        try:
            addTopic.save()
        except:
            pass 
        return new_cat_id
    else:
        return tlist[0][0]     
    
def get_thread_children(parentThread):
    pass

def get_all_threads():
    pass

def save_topic(topic):
    pass

def save_thread(thread):
    pass

"""
# @author Muhammad Umair
# e.g. << this method is to get all data from medicalcontent w.r.t title
# @author umair - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author umair - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def get_medicalcontent(alpha,subcontent,product):
    subcontent2 = ''
    cursor= connection.cursor()
    alpha=str(alpha)
    query = "Select * from medicalcontent_data as md where md.title like '"+alpha+"%' AND md.language='en' "
    if subcontent != None and subcontent != '':
        text_list = subcontent.split(" ")
        for item in text_list:
            subcontent2 += item.capitalize() +" "
        subcontent2 = str(subcontent2).rstrip()
        query += " AND (md.subcontent='"+subcontent2+"' OR md.subcontent='"+subcontent+"')"
    if product!=None and product!='':
        query+=" AND (md.product='"+product+"')"   
    cursor.execute(query)
    articles = cursor.fetchall()
    return articles

"""
# @author Muhammad Imran
# e.g. << this method is to get products and subcontent. 
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""
def get_articlescontent():
    cursor= connection.cursor()
    cursor.execute("select product,subcontent from medicalcontent_data where language='en' limit 10")
    #tlist = cursor.fetchall()
    return cursor.fetchall()

"""
# @author Muhammad Imran
# e.g. << this method is to get title,projectid and gencontentid.
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def get_titlesubcontents(text):
    cursor=connection.cursor()
    cursor.execute("select title,projectid,gencontentid from medicalcontent_data where subcontent='%s' AND language='en' AND length(title) < 35 limit 16"%text)
    return cursor.fetchall()


"""
# @author Muhammad Imran
# e.g. << this method is to get product,projectid and gencontentid.
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author imran - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def get_featuredContent():
    #cursor=connection.cursor()
    #cursor.execute("select product,projectid,gencontentid from medicalcontent_data limit 5")
    #return cursor.fetchall()

    return [
        ("HIE Multimedia", "1", "002455",5),
        ("HIE Multimedia", "1", "000541",2),
        ("HIE Multimedia", "1", "000894",3),
        ("HIE Multimedia", "1", "000442",4),
        ("HIE Multimedia", "1", "000147",1) 
       ]
    
def get_articleinfo(projectid,gencontentid):
    cursor=connection.cursor()
    cursor.execute("select product,subcontent,title from medicalcontent_data where language='en' and projectid='"+projectid+"' and gencontentid='"+gencontentid+"'")
    return cursor.fetchall()
"""
# @author Muhammad Umair
# e.g. << this method is to get all records from medicalcontent w.r.t specific product,title and subcontent 
# @author umair- FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author umair - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def get_search_record(search_text,subcontent):
    search_text2 = ''
    text_list = search_text.split(" ")
    cursor= connection.cursor()
    for item in text_list:
        search_text2 += item.capitalize() +" "
    search_text = str(search_text)
    search_text2 = str(search_text2).rstrip()
    query = "select * from medicalcontent_data where language='en' "
    if subcontent == '':
        query += " and title like '%"+search_text+"%' "
        query += " or subcontent like '%"+search_text+"%' or product like '%"+search_text+"%' "
        query += " or title like '%"+search_text2+"%' or subcontent like '%"+search_text2+"%' "
        query += " or product like '%"+search_text2+"%' "
    
    if subcontent != '':
        query += " and title like '%"+search_text+"%' or title like '%"+search_text2+"%' AND subcontent = '"+subcontent+"' "
    query += " order by product,title,subcontent "
    cursor.execute(query)
    search_record = cursor.fetchall()
    return search_record

def get_search_record_center(search_text,center,area):
    query = "select * from medicalcontent_center where upper(center) = upper('"+center+"') and ('"+area+"' = '' OR upper(area) = upper('"+area+"')) and upper(articletitle) like upper('%"+search_text+"%') order by area, articletitle;"
    cursor= connection.cursor()
    cursor.execute(query)
    search_record = cursor.fetchall()
    return search_record

def get_breadcrumb(subcontent):
    cursor=connection.cursor()
    cursor.execute("select product from medicalcontent_data where language='en' and subcontent='"+subcontent+"'")
    return cursor.fetchall()


def get_medicalcontent_center():
    cursor=connection.cursor()
    cursor.execute("select DISTINCT center as center from medicalcontent_center order by center")
    return cursor.fetchall()

def get_medicalcontent_areas(center):
    cursor=connection.cursor()
    cursor.execute("select DISTINCT area as area from medicalcontent_center where upper(center) = upper('%s') and area is not null order by area" %center)
    return cursor.fetchall()

def get_medicalcontent_article(area):
    cursor=connection.cursor()
    cursor.execute("select articletitle, targeturl  from medicalcontent_center where upper(area) = upper('%s') order by articletitle limit 10" %area)
    return cursor.fetchall()

def get_medicalcontent_area(center, area):
    cursor=connection.cursor()
    cursor.execute("select articletitle, targeturl  from medicalcontent_center where upper(center) = upper('"+ center +"') and upper(area) = upper('"+ area +"') order by articletitle")
    return cursor.fetchall()

def get_medicaldata_subcontents():
    cursor=connection.cursor()
    cursor.execute("select DISTINCT subcontent from medicalcontent_data where language='en' order by subcontent")
    return cursor.fetchall()

def update_news_model(feed_url):
    feed = feedparser.parse(feed_url)
    entries = feed['entries']
    
    for each_entry in entries:
        try:
            splits = each_entry['summary_detail']['value'].split('<p class="lead">')
            if len(splits) < 2:
                splits = each_entry['summary_detail']['value'].split('<p class="notice">')
                
            f_title = each_entry['title']
            f_summary = splits[1][:160]
            f_body = '<p>' + splits[1]

            # Extract author name if available
            #---------------------------------------------------------------------
            split_entry = splits[0].split('<p class="byline">')
            if not len(split_entry)<2:
                by = split_entry[1][0:split_entry[1].index('</p>')]
            else:
                try:
                    check_author = split_entry[0][split_entry[0].index('<p>')+3:-5]
                except ValueError:
                    check_author = []
                    
                if len(check_author)>0:
                    by = check_author
                else:
                    by=None
            #---------------------------------------------------------------------

            last_updated = parse(split_entry[0][split_entry[0].index('20'):
                                                split_entry[0].index('Last Updated:')+39])
            news_id = uuid.uuid4()
            #news_image=[]
            #try:
            #    news_image = urllib.urlretrieve('http://someimageURL',
            #                       'someFilePath\\tmp\\FileName')
            #except:
            #    pass
#            if news_image:
#                model_news_image = File(open(news_image[0],'rb'))
#            else:
            #model_news_image = File(open(settings.MEDIA_ROOT+"\\images\\media\\news1.png",'rb'),str(news_id)+'_image.png')
            
            newsItem.objects.get(title = f_title, 
                                 summary = f_summary, 
                                 datetime_created = last_updated,
                                 author=by)
        except newsItem.DoesNotExist:

            new_news_item = newsItem(id=news_id,
                                     title=f_title,
                                     summary=f_summary,
                                     body=f_body,
                                     author=by,
                                     datetime_created=last_updated,
                                     #image = model_news_image,
                                     last_viewed = parse('2010-01-01 00:00:00+05')
                                     )
            try:
                new_news_item.save()
                #model_news_image.close()
                #if news_image:
                #    os.remove(news_image[0])
            except:
                pass
        except:
            pass
        
def get_news_top_thread(id):
    cursor= connection.cursor()
    cursor.execute("""SELECT t.id, t.thread_name, t.thread_body, u.nickname, text(''), t.parent_thread_id, t.topic_id, text(''),text(''), (select date_part('days',(current_date - t.datetime_created ))):: bigint as days_diff,  (select date_part('hours',(current_timestamp - t.datetime_created )))::bigint as hours_diff, t.datetime_created, t.most_popular ,t.owner_id, t.is_locked
        FROM forum_thread AS t, user_user AS u where t.parent_news_id = '"""+id+"'")
    news_list = cursor.fetchall()
    return news_list


def get_condition():
    cursor= connection.cursor()
    cursor.execute("""select level_3 from adamcontent_data where level_2 = 'Conditions A-Z' AND lang = 'en'group by level_3,order_3 order by order_3""")
    condition = cursor.fetchall()
    return condition


def get_condition_article(condition):
    cursor= connection.cursor()
    cursor.execute("select split_part(level_5,'/',2)||'/'||split_part(level_5,'/',3)as level_5,title from adamcontent_data where level_2 = 'Conditions A-Z' AND lang = 'en' AND level_3 = '"+unicode(condition)+"' order by level_5 limit 10")
    articles = cursor.fetchall()
    return articles
"""
# @author Muhammad Imran
# desc << 
# e.g. << Get distinct subcontents for video categories
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""
def get_video_categories():
    cursor=connection.cursor()
    cursor.execute("select subcontent from medicalcontent_video where video_type='mov' and language='en' group by subcontent")
    return cursor.fetchall()



def get_condition_article_alphabet(alpha,condition):
    cursor= connection.cursor()
    alpha=str(alpha)
    query = "Select level_2,level_5,title from adamcontent_data as ad where ad.title like '"+alpha+"%' "
    query+= " AND (ad.level_2='"+condition+"')"   
    cursor.execute(query)
    articles = cursor.fetchall()
    return articles

"""
# @author Muhammad Imran
# desc << 
# e.g. << Get videos for specific category
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""
def get_eachCategory_videos(subcontent):
    cursor=connection.cursor()
    cursor.execute("select videoid,title,video_type,subcontent from medicalcontent_video where video_type='mov' AND subcontent='"+subcontent+"' AND language='en' group by videoid,title,video_type,subcontent limit 20")
    return cursor.fetchall()

