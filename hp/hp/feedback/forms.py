from django import forms
from django.forms.widgets import Widget, Textarea
from django.conf import settings

class feedback_form(forms.Form):
    user_id = forms.CharField(label="user",widget=forms.HiddenInput())
    path = forms.CharField(label="user",widget=forms.HiddenInput())
    feedback_text = forms.CharField(required = False,label="",widget=forms.Textarea(attrs={'cols' : "40", 'rows': "5",'class':'input_textarea' }))
    type_feedback =forms.ChoiceField(required = False,choices=[
                                              ('Bug','Bug'),
                                              ('Suggestion', 'Suggestion'),
                                              ('Comment','Comment')],label="",widget=forms.CheckboxSelectMultiple(attrs={'class':'input_checkbox' }))