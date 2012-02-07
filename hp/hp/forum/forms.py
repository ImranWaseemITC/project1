from django import forms
from hp.forum.models import topic as topic
from django.conf import settings

class new_thread_form(forms.Form):
    thread_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_txt'}),max_length=30, required = False)
    thread_body = forms.CharField(widget=forms.Textarea(attrs={'class':'ckeditor'}))
    keywords = forms.CharField(widget=forms.TextInput(attrs={'class':'input_txt'}),max_length=30, required=False)
    category_id =forms.ModelChoiceField(queryset=topic.objects.order_by("topic_name"), empty_label="", required=False,label="Choose a category")
    new_category = forms.CharField(widget=forms.TextInput(attrs={'class':'input_txt'}),max_length=30, required = False,label="or Create a Category")
	#File field added by Anwar
   # docfile = forms.FileField(required=False, label='Select a file', help_text='max. 2 megabytes')
    
    class Media:
         
        js = (settings.MEDIA_URL + settings.CKEDITOR_MEDIA_PREFIX + 'ckeditor/ckeditor.js',)
	
class search_form(forms.Form):
    search_text = forms.CharField(widget = forms.TextInput(attrs={'class':'input_keyword'}))
    category_choices=forms.ModelChoiceField(queryset=topic.objects.order_by("topic_name"), empty_label="All Forums", required=False)
    
class edit_category_form(forms.Form):
    category_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_txt'}), max_length=30, label="Category Name")
    category_body = forms.CharField(widget=forms.Textarea(attrs={'class':'input_textarea'}), required=False, label="Category Body")
    category_keywords = forms.CharField(widget=forms.TextInput(attrs={'class':'input_txt'}), max_length=30, required=False, label="Keywords")
   
class edit_thread_form(forms.Form):
    thread_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input_txt'}),max_length=30, required = False)
    thread_body = forms.CharField(widget=forms.Textarea(attrs={'class':'input_textarea ckeditor','onclick':'get_csrf_token_for_category()'}))
    keywords = forms.CharField(widget=forms.TextInput(attrs={'class':'input_txt'}),max_length=30, required=False)
    #category_id =forms.ModelChoiceField(queryset=topic.objects.all(), empty_label="", required=False,label="Choose a category")
    #File field added by Anwar
    #docfile = forms.FileField(required=False, label='Select a file', help_text='max. 2 megabytes')
    
    class Media:
         
        js = (settings.MEDIA_URL + settings.CKEDITOR_MEDIA_PREFIX + 'ckeditor/ckeditor.js',)