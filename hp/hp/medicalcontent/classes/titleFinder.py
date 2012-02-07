"""
# @author Muhammad Umair
# This class is used to find title and break into trigrams
"""
from pycassa.columnfamily import ColumnFamily
from pycassa.pool import ConnectionPool
from pycassa.index import *
#import xml.dom
from xml.dom import minidom, Node
import uuid

class titleFinder(object):
    
    def __init__(self):
        self.functionList = []
        self.attributeList = ['title','Title','titleContent']
        self.specialCharactersList = [':']
        self.tagList = ['p','h1','h2','h3','h4','b']
        self.maxTitleSize = 100
        self.occurance = 0
        self.DbConnection = ConnectionPool('hp')
        self.TEMP_TITLE_SCORE = ColumnFamily(self.DbConnection, 'tempTitleScore')
        self.functionList.append(self.getTitleEx)
        self.functionList.append(self.getTitleContent)
    
    xmlNode = ""
  
    def getTitle(self, xmlNode, titleList):
        for fn in self.functionList:
            fn(xmlNode, titleList)
      
    #
    # write new parsers
    #
  
    def getTitleEx(self, nodelist, titleList):
        if nodelist == None:
            return
        if nodelist.nodeType == Node.ELEMENT_NODE:
            self.occurance +=1
            for t in self.attributeList:
                if nodelist.getAttribute(t) or nodelist.getAttribute(t) != "":
                    titleList.append(nodelist.getAttribute(t))
                    self.TEMP_TITLE_SCORE.insert(uuid.uuid1(),{'title':nodelist.getAttribute(t),'tag':nodelist.nodeName,'score':10,'occurance':self.occurance})
        if nodelist.nodeType == Node.TEXT_NODE:
            score = 0
            d = nodelist.data
            score = self.checkTitle(d, nodelist.parentNode.nodeName)
            if score > 2 :
                self.TEMP_TITLE_SCORE.insert(uuid.uuid1(),{'title':d,'tag':nodelist.parentNode.nodeName,'score':score,'occurance':self.occurance})
                titleList.append(d)    
        for nl in nodelist.childNodes:
            self.getTitleEx(nl, titleList)
        return ""
    
    
    def getTitleContent(self, nodelist, titleList):
        if nodelist == None:
            return
        if nodelist.nodeType == Node.ELEMENT_NODE:
            self.occurance +=1
            for t in self.attributeList:
                if nodelist.getAttribute(t) or nodelist.getAttribute(t) != "":
                    titleList.append(nodelist.getAttribute(t))
        if nodelist.nodeType == Node.TEXT_NODE:
            score = 0
            d = nodelist.data
            score = self.checkTitle(d, nodelist.parentNode.nodeName)
            if score > 2 :
                titleList.append(d)    
        for nl in nodelist.childNodes:
            self.getTitleEx(nl, titleList)
        return ""
    
    
    def checkTitle(self,title,nodeName):
        tempScore = 0
        if len(title) < self.maxTitleSize:
            tempScore = 2
            for c in self.specialCharactersList:
                if title.find(c) != -1:
                    tempScore +=2
            for t in self.tagList:
                if t == nodeName:
                    tempScore +=2
        return tempScore 
    
    def getTrigrams(self,title):
        trigrams = {}
        for index in range(len(title)-2):
            trigram =""
            trigram = title[index:index+3]
            if trigrams.has_key(trigram) :
                trigrams[trigram] = trigrams[trigram] + 1
            else:
                trigrams[trigram] = 1
        return trigrams