from django import forms
from hp.groupmanager.models import group as Group
from hp.user.models import user as User
from django.forms.widgets import Widget, Textarea

"""
# @author Mohsin Aijaz
"""


class CreateGroupForm(forms.Form):
    
    '''
    # The CreateGroupForm Class provides form to save
    # Group name & Description.
    '''
    
    name = forms.CharField(max_length=30, label='Name')
    description = forms.CharField(required=False, label='Description', widget=forms.Textarea)
    
class DeleteGroupForm(forms.Form):
    
    '''
    # The DeleteGroupForm Class provides form to Delete
    # Group(s). Groups are displayed as checkboxes.
    '''
        
    group_id = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, label='')

class AddUsersToGroupForm(forms.Form):
    
    '''
    # The AddUsersToGroupForm Class provides form to 
    # Add/Remove Users from Group. Groups are displayed
    # in comboxbox and Users as checkboxes.
    '''
    
    group_id = forms.ModelChoiceField(queryset=Group.objects.all(), label='Group')
    user_id = forms.ModelMultipleChoiceField(required=False, queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple, label='User')
    myHiddenField = forms.BooleanField(widget = forms.HiddenInput(attrs={'id':'myHiddenFieldValue'}), required=False)
    

        
       

