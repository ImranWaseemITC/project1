"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django.http import Http404,HttpResponse
from django.template import RequestContext
from django.conf import settings
import xml.dom.minidom
from hp.dbfuncs import *
from django.shortcuts import render_to_response
from hp.medicalcontent.model import customModels
from hp.medicalcontent.model import metaData
from hp.hp_utils import is_userLogged
import os

"""
# @author Muhammad Imran
# desc << 
# e.g. << this is to parse xml and show data on articles page
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def getArticleContentByProductIDArticleID(request, productID, articleID):
    """
    # URL recieved e.g. http://healthpark.ca/99/9999
    """

    artical = customModels.MArtical()
    artical.video_list = []    
    artical.content_list = []

    artical.related_list = []
    artical.image_list=[]
    error_list=[]

    xmlpath = settings.XML_ROOT.replace('\\','/')
    mediapath = settings.MEDIA_ROOT.replace('\\','/')
    try:
        
        articleInfo = get_articleinfo(productID, articleID)
        
        if articleInfo:
            product = unicode(articleInfo[0][0])
            doc = xml.dom.minidom.parse(xmlpath + "/" + product + "/" + productID + "/" + articleID+".xml")
            subcontent = unicode(articleInfo[0][1])
            title = unicode(articleInfo[0][2])
        else:
            raise Http404("The page You requested was not found")
        
    except IOError:
        raise Http404("The page You requested was not found")
    
    
    # if XML file found then parser
    
    # get Header
    for node in doc.getElementsByTagName("adamContent"):
        artical.headerTitle = node.getAttribute("title")
        artical.headerSubContent = node.getAttribute("subContent")
        
    # get Content
    for node in doc.getElementsByTagName("textContent"):
        for textNode in doc.getElementsByTagName("textLink"):
            if textNode:
                pid=textNode.getAttribute("projectTypeID")
                gid=textNode.getAttribute("genContentID")
                extlink=textNode.getAttribute("extLink")
                if not pid=="" and not gid=="":
                    link = doc.createElement("a")
                    
                    if request.is_secure():
                        hrefString = "https://" + request.get_host()+'/' +'adamcontent'+'/'+pid+'/'+gid+'/'
                    else:
                        hrefString = "http://" + request.get_host()+'/' +'adamcontent'+'/'+pid+'/'+gid+'/'
                    
                    link.setAttribute("href", hrefString)
                    
                    for t in textNode.childNodes:
                        if t.nodeType == t.TEXT_NODE:
                            link.appendChild(t)
                    
                    #add this new anchor
                    textNode.parentNode.replaceChild(link, textNode)
                """if not extlink=="":
                    link.setAttribute("href", extlink)
                    
                    for t in textNode.childNodes:
                        if t.nodeType == t.TEXT_NODE:
                            link.appendChild(t)
                    
                    #add this new anchor
                    textNode.parentNode.replaceChild(link, textNode)"""
                    
        #Inline VisualContent display            
        """for visualNode in doc.getElementsByTagName("visualContent"):
            if visualNode:
                    if visualNode.getAttribute("mediaType")=="jpg" or visualNode.getAttribute("mediaType")=="gif" or visualNode.getAttribute("mediaType")=="png":
                        images =  customModels.MArtical.imageContent()
                        images.imageID=visualNode.getAttribute("genContentID")
                        images.imageType=visualNode.getAttribute("mediaType")
                        artical.image_list.append(images)
                        for node in visualNode:
                            if visualNode.childNodes:
                                link = doc.createElement("a")
                                pid=visualNode.childNodes[0].getAttribute("projectTypeID")
                                gid=visualNode.childNodes[0].getAttribute("genContentID")
                                hrefString = "http://" + request.get_host()+'/'+'adamcontent/'+pid+'/'+gid+'/'
                                link.setAttribute("href", hrefString)
                                image = doc.createElement("img")
                                imageSource='/media/graphics/images/en/'+visualNode.getAttribute("genContentID")+'.'+visualNode.getAttribute("mediaType")
                                image.setAttribute("src", imageSource)
                                image.setAttribute("width","100")
                                image.setAttribute("height","100")
                                link.appendChild(image)
                                add this image
                                visualNode.parentNode.replaceChild(link, visualNode)
                    if visualNode.getAttribute("mediaType")=="swf" or visualNode.getAttribute("mediaType")=="flv" :
                        video = customModels.MArtical.videoContent()
                        video.videoFolder=node.getAttribute("genContentID")
                        video.videoID=node.getAttribute("genContentID")+'.'+node.getAttribute("mediaType")
                        artical.video_list.append(video)"""
                        
        cv = customModels.MArtical.contentView()
        if not "*" in unicode(node.getAttribute("title")):
            cv.title = node.getAttribute("title")     

        cv.content = node.toxml()
        artical.content_list.append(cv)
        
    

    # get Related Item
    for node in doc.getElementsByTagName("relatedItems"):
        if node.getAttribute('type') == 'readMore':
            for nodeRelated in doc.getElementsByTagName("item"):
                cv = customModels.MArtical.contentView()
                cv.projectTypeID = nodeRelated.getAttribute("projectTypeID")
                cv.genContentID = nodeRelated.getAttribute("genContentID")
                cv.title = nodeRelated.getAttribute("Title")
                artical.related_list.append(cv)

    # get footer
    for node in doc.getElementsByTagName("versionInfo"):
        artical.footerReviewDate = node.getAttribute("reviewDate")
        artical.footerReviewBy = node.getAttribute("reviewedBy")
        
        
    # get Article video
    for visualNode in doc.getElementsByTagName("visualContent"):
        if visualNode:
            if visualNode.getAttribute("mediaType")=="jpg" or visualNode.getAttribute("mediaType")=="png" or  visualNode.getAttribute("mediaType")=="gif":
                images =  customModels.MArtical.imageContent()
                images.imageID=visualNode.getAttribute("genContentID")
                images.imageType=visualNode.getAttribute("mediaType")
                artical.image_list.append(images)
            if visualNode.getAttribute("mediaType")=="mov" or visualNode.getAttribute("mediaType")=="flv" or visualNode.getAttribute("mediaType")=="swf" or visualNode.getAttribute("mediaType")=="dcr":
                video=customModels.MArtical.videoContent()
                video.videoFolder=visualNode.getAttribute("genContentID")
                if visualNode.getAttribute("mediaType")=="mov":
                    video.videoID=visualNode.getAttribute("genContentID")+".flv"
                    filepath=mediapath+"/graphics/multimedia/en/"+video.videoFolder+"/"+video.videoID
                    if os.path.exists(filepath):
                        artical.video_list.append(video)
                    else:
                        error_list.append("Video not found")    
                if visualNode.getAttribute("mediaType")=="flv":
                    video.videoID=visualNode.getAttribute("genContentID")+"."+visualNode.getAttribute("mediaType")
                    filepath=mediapath+"/graphics/multimedia/en/"+video.videoFolder+"/"+video.videoID
                    if os.path.exists(filepath):
                        artical.video_list.append(video)
                    else:
                        error_list.append("Video not found")    
                if visualNode.getAttribute("mediaType")=="swf":
                    video.videoID=visualNode.getAttribute("genContentID")+"."+visualNode.getAttribute("mediaType")
                    filepath=mediapath+"/raphics/multimedia/en/"+video.videoFolder+"/"+video.videoID
                    if os.path.exists(filepath):
                        artical.video_list.append(video)
                    else:
                        error_list.append("Video not found")      
                if visualNode.getAttribute("mediaType")=="dcr":
                    video.videoID=visualNode.getAttribute("genContentID")+"."+visualNode.getAttribute("mediaType")
                    filepath=mediapath+"/graphics/multimedia/en/"+video.videoFolder+"/"+video.videoID
                    error_list.append("Video Format not Supported")         
                  
    user_status = is_userLogged(request)                  
    return render_to_response('medicalcontent/inner.html', {'MArtical': artical,'productID':productID,'articleID':articleID,'product':product,'subcontent':subcontent,'title':title,'error_list':error_list,'user_isLogged':user_status},context_instance=RequestContext(request))
    

def content(request,alpha):
    subcontent = ''
    templateHeader=''
    product=''
    breadcrumbProduct=''
    count=0
    if request.method == "GET":
        if request.GET.get("subcontent"):
            subcontent = request.GET.get("subcontent")
            breadcrumbProductInfo=get_breadcrumb(subcontent)
            breadcrumbProduct=unicode(breadcrumbProductInfo[0][0])
            templateHeader=subcontent.capitalize()
        if request.GET.get("product"):
            product=request.GET.get("product")
            breadcrumbProduct=product   
    alphabets = []
    recordSet = {}
    recordSet1 = {}
    recordSet2 = {}
    upperalpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    upperalpha_list=list(upperalpha)
    loweralpha="abcdefghijklmnopqrstuvwxyz"
    loweralpha_list=list(loweralpha)
    alphabets.append(alpha)
    for item in loweralpha_list:
        alphabets.append(alpha + item)
    for item in alphabets:
            rows = get_medicalcontent(item,subcontent,product)
            if len(rows) > 0:
                recordSet[item] = rows
    for item in recordSet:
        count=count+1
        if count<=((len(recordSet)+1)/2):
            recordSet1[item]=recordSet[item]
        else:
            recordSet2[item]=recordSet[item]                
                   
    return render_to_response('medicalcontent/content.html',{'upperalpha_list':upperalpha_list,'loweralpha_list':loweralpha_list,'a':alpha,'rs1':recordSet1,'rs2':recordSet2,'subcontent':subcontent,'tHead':templateHeader,'product':product,'bProduct':breadcrumbProduct, 'subcontents':get_medicaldata_subcontents()},context_instance=RequestContext(request))

def displaycenters(request):
    
    center = ""
    area = ""
    if request.method == "GET":
      

        
        if request.GET.get("center"):
            center = request.GET.get("center")
            center = center.replace("'", "''")
            
        if request.GET.get("area"):
            area = request.GET.get("area")
            area = area.replace("'", "''")
            
    if center == '' and area == '':
        centers=get_medicalcontent_center()
                    
        return render_to_response('allcenter.html',{'centers':centers},context_instance=RequestContext(request))
    
    if center != '' and area== '':
        areas=get_medicalcontent_areas(center)
        center = center.replace("''", "'")
        articles = {}
        for eacharea in areas:        
            articles[eacharea[0]] = get_medicalcontent_article(eacharea[0])
            
        return render_to_response('center.html',{'articles':articles,'center':center},context_instance=RequestContext(request))
    
    if area != '':

        areaarticles=get_medicalcontent_area(center, area)
        center = center.replace("''", "'")
        area = area.replace("''", "'")
       
        return render_to_response('area.html',{'areaarticles':areaarticles, 'center':center, 'area':area,'totrecords':len(areaarticles)/2},context_instance=RequestContext(request))


"""
# @author Muhammad Imran
# desc << 
# e.g. << View to call selected video
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def video(request):
    video=''
    if request.method == "GET":
        if request.GET.get("video"):
            video=request.GET.get("video")
        if request.GET.get("text"):
            video_text=request.GET.get("text")   
    return render_to_response('video.html',{'video':video,'video_text':video_text},context_instance=RequestContext(request))


"""
# @author Muhammad Imran
# desc << 
# e.g. << View to display videos w.r.t to categories
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""

def allvideo(request):
    mediapath = settings.MEDIA_ROOT.replace('\\','/')
    artical = customModels.MArtical()
    artical.allvideo_list = []
    artical.allcategory_list=[]
    artical.allcategory_list=get_video_categories()
    existed_category_list=[]
    distinct_category_list=[]
    if artical.allcategory_list:
        for category in artical.allcategory_list:
            allcatvideos=get_eachCategory_videos(unicode(category[0]))
            if allcatvideos:
                for videoid,video_desc,video_type,subcontent in allcatvideos:
                    filepath=mediapath+"/graphics/multimedia/en/"+videoid+"/"+videoid+".flv"
                    if os.path.exists(filepath):
                         allvideo=customModels.MArtical.allvideoContent()
                         allvideo.videoID=unicode(videoid)
                         allvideo.videoDesc=unicode(video_desc)
                         allvideo.videoType=unicode(video_type)
                         allvideo.videoCategory=(unicode(subcontent)).capitalize()
                         existed_category_list.append((unicode(subcontent)).capitalize())
                         artical.allvideo_list.append(allvideo)
    if existed_category_list:             
        for item in existed_category_list:
            if item not in distinct_category_list:
                distinct_category_list.append(item)
                
    return render_to_response('allvideo.html',{'MArtical': artical,'distinct_category_list':distinct_category_list},context_instance=RequestContext(request))

