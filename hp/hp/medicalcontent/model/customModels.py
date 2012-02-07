"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""


"""
# @author Waqar Azeemm
# e.g. << this is just as an sample, to get feedback.
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BF [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""
class MArtical(object):
    """
    #
    # modal class to hold the article read from XML
    #
    """
    class contentView(object):
        title = ""
        content = ""
    
    class relatedTopics(object):
        genContentID = ""
        projectTypeID = ""
        title = ""
    
    class videoContent(object):
        videoID=""
        videoFolder=""  
     
    class imageContent(object):
        imageID=""
        imageType="" 
    
    class allvideoContent(object):
        videoID=""
        videoDesc=""
        videoType=""
        videoCategory=""     
    product = ""
    article = ""

    headerTitle = ""
    headerSubContent = ""

    footerReviewDate = ""
    footerReviewBy = ""

    # list(s) for images and other stuff
    content_list = []
    related_list = []
    video_list=[]
    image_list=[]
    allvideo_list=[]
    allcategory_list=[]  
    """class MArtical END""" 


