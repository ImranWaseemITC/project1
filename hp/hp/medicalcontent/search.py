from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from hp.dbfuncs import get_search_record,get_search_record_center

@csrf_protect
def search(request):
    errors = []
    count=0
    search_text = ''
    subcontent = ''
    search_record = []
    search_record1=[]
    search_record2=[]
    if request.method == "POST":
        if not request.POST.get('search_input', ''):
            errors.append('Enter text to search.')
        if not errors:
            search_text = request.POST["search_input"]
            search_record = get_search_record(search_text,subcontent)
            if search_record:
                for item in search_record:
                    count=count+1
                    if count<=((len(search_record)+1)/2):
                        search_record1.append(item)
                    else:
                        search_record2.append(item) 
            
    return render_to_response('medicalcontent/search.html',{'search_record1':search_record1,'search_record2':search_record2,'errors':errors,"subcontent":subcontent},context_instance=RequestContext(request))

@csrf_protect
def searchByCategory(request):
    errors = []
    count=0
    search_text = ''
    subcontent = ''
    search_record = []
    search_record1=[]
    search_record2=[]
    if request.method == "POST":
        if not errors:
            subcontent = request.POST["subcontent"]
            search_text = request.POST["search_input"]
            search_record = get_search_record(search_text,subcontent)
            if search_record:
                for item in search_record:
                    count=count+1
                    if count<=((len(search_record)+1)/2):
                        search_record1.append(item)
                    else:
                        search_record2.append(item) 
                        
    return render_to_response('medicalcontent/search.html',{'search_record1':search_record1,'search_record2':search_record2,'errors':errors,"subcontent":subcontent},context_instance=RequestContext(request))
    
    
@csrf_protect
def searchBySubcontent(request):
    errors = []
    count=0
    search_text = ''
    subcontent = ''
    search_record = []
    search_record1=[]
    search_record2=[]
    if request.method == "POST":
        if not request.POST.get('search_input', ''):
            errors.append('Enter text to search.')
        if not errors:
            subcontent = request.POST["subcontent"]
            search_text = request.POST["search_input"]
            search_record = get_search_record(search_text,subcontent)
            
            if search_record:
                for item in search_record:
                    count=count+1
                    if count<=((len(search_record)+1)/2):
                        search_record1.append(item)
                    else:
                        search_record2.append(item)   
                
    return render_to_response('medicalcontent/search.html',{'search_record1':search_record1,'search_record2':search_record2,'errors':errors,"subcontent":subcontent},context_instance=RequestContext(request))

@csrf_protect
def searchByCenter(request):
    errors = []
    count=0
    search_text = ''
    center = ''
    search_record = []
    search_record1=[]
    search_record2=[]
    if request.method == "POST":
        if not request.POST.get('search_input', ''):
            errors.append('Enter text to search.')
        if not errors:
            center = request.POST["center"]
            center = center.replace("'", "''")
            search_text = request.POST["search_input"]
            area = request.POST["area"]
            search_record = get_search_record_center(search_text,center,area)
            
            if search_record:
                for item in search_record:
                    count=count+1
                    if count<=((len(search_record)+1)/2):
                        search_record1.append(item)
                    else:
                        search_record2.append(item)   
                
    return render_to_response('medicalcontent/searchcenter.html',{'search_record1':search_record1,'search_record2':search_record2,'errors':errors,"center":center},context_instance=RequestContext(request))       