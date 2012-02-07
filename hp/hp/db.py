from django.conf import settings
from django.http import Http404,HttpResponse,HttpResponseServerError
import psycopg2

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

class dbConnection(object):
    
    def __init__(self):
        self.dbname = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.host = DB_HOST 
        self.error = "error"

    def connect(self):
        try:
            conn = psycopg2.connect("dbname='"+self.dbname+"' user='"+self.user+"' host='"+self.host+"' password='"+self.password+"'")
        except Exception , err:
            raise Http404("Database connection failed")
        return conn