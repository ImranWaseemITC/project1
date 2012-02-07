"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django.template import RequestContext
from hp.dbfuncs import get_condition,get_condition_article,get_condition_article_alphabet
from django.shortcuts import render_to_response


def conditions(request):
    condition_article = {}
    condition = get_condition()
    for cond in condition:
            for c in cond :
                condition_article[c] = get_condition_article(c)
    return render_to_response('conditions.html',{'condition':condition_article,'cond':condition},context_instance=RequestContext(request))

def browse_condition(request,condition,alpha):
    count=0
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
            rows = get_condition_article_alphabet(item,condition)
            if len(rows) > 0:
                recordSet[item] = rows
    for item in recordSet:
        count=count+1
        if count<=((len(recordSet)+1)/2):
            recordSet1[item]=recordSet[item]
        else:
            recordSet2[item]=recordSet[item]                
                   
    return render_to_response('medicalcontent/condition_browse.html',{'upperalpha_list':upperalpha_list,'loweralpha_list':loweralpha_list,'a':alpha,'rs1':recordSet1,'rs2':recordSet2},context_instance=RequestContext(request))