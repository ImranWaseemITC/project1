"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django import http
from django.http import HttpResponseRedirect

"""
# @author Anwar Ullah
# e.g. << this is just as an sample, to get feedback.
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
# @see FR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see BR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @see CR [ 0123456789 ] Is necessary create method to get ID menu use menu Name http://healthpark.ca/tracker/index.php?func=detail&aid=1966326&group_id=176962&atid=879335
# @author waqar - FR: [ 2214883 ] Remove SQL code and Replace for Query
"""
class UserAuthentication(object):

    def process_request(self, request):
        
        try:
            if request.path=='/':
                return None
            
            if request.session['User_id']:
                return None

        except KeyError:
            return HttpResponseRedirect('/')

