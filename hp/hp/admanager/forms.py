from django import forms
from hp.admanager.models import adclient as Adclient, internalad as Internalad, externalad as Externalad, adpool as Adpool
from django.forms.widgets import Widget, Textarea
from django.forms.extras.widgets import SelectDateWidget

"""
# @author Mohsin Aijaz
"""


class CreateAdClient(forms.Form):
    
    '''
    # The CreateAdClient Class will display
    # form to save client object. It contains
    # CLient name and description 
    '''
    
    name = forms.CharField(max_length=30, label='Name')
    description = forms.CharField(required=False, label='Description', widget=forms.Textarea)
    
class AddInternalAd(forms.Form):
    
    '''
    # The AddInternalAd Class will display
    # form to save internal ads with necessary 
    # information needed to display it 
    '''
    
    campaignName = forms.CharField(max_length=30, label='Campaign Name')
    contentSpecific = forms.CharField(max_length=30, label='Content Specific')
    keywords = forms.CharField(max_length=30, label='Keywords')
    activeDate = forms.DateField(label='Active Date(mm/dd/yyyy)',  widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    expiredDate = forms.DateField(label='Expired Date(mm/dd/yyyy)', widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    noOfImpressions = forms.IntegerField(label='# of Impressions')
    priority = forms.IntegerField(label='Priority')
    maxImpressions = forms.IntegerField(label='Max. Impressions')
    targetpages = forms.CharField(label='Target Pages', widget=forms.Textarea)
    ad = forms.CharField(label='Ad', widget=forms.Textarea)
    adType = forms.ChoiceField(choices=[('Image','(300 x 250)'),
                                        ('Banner1', '(160 x 600)'),
                                        ('Banner2', '(728 x 90)')],
                                widget=forms.RadioSelect)   

class AddExternalAd(forms.Form):
            
    '''
    # The AddExternalAd Class will display
    # form to save external ads with necessary 
    # information needed to display it.
    # The Client of external ad will be displayed
    # in combobox 
    '''
    
    adclient_id = forms.ModelChoiceField(queryset=Adclient.objects.all(), label='Client')
    campaignName = forms.CharField(max_length=30, label='Campaign Name')
    contentSpecific = forms.CharField(max_length=30, label='Content Specific')
    keywords = forms.CharField(max_length=30, label='Keywords')
    activeDate = forms.DateField(label='Active Date',  widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    expiredDate = forms.DateField(label='Expired Date',  widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    noOfImpressions = forms.IntegerField(label='# of Impressions')
    priority = forms.IntegerField(label='Priority')
    maxImpressions = forms.IntegerField(label='Max. Impressions')
    targetPages = forms.CharField(label='Target Pages', widget=forms.Textarea)
    adCode = forms.CharField(max_length=30, label='Ad Code')
    ad = forms.CharField(label='Ad', widget=forms.Textarea)
    adType = forms.ChoiceField(choices=[('Image','(300 x 250)'),
                                        ('Banner1', '(160 x 600)'),
                                        ('Banner2', '(728 x 90)')],
                                widget=forms.RadioSelect)  

class CreateAdPool(forms.Form):
    
    '''
    # The CreateAdPool Class will display
    # form to save ads so that the adpool
    # will be populated manually and 
    # ads will be dipslayed from adpool 
    # whereever necessary
    '''
    
    campaignName = forms.CharField(max_length=30, label='Campaign Name')
    ad = forms.CharField(label='Ad', widget=forms.Textarea)
    targetPages = forms.CharField(label='Target Pages', widget=forms.Textarea) 
    adType = forms.ChoiceField(choices=[('Image','Image'),
                                        ('Banner1', 'Banner1'),
                                        ('Banner2', 'Banner2')],
                                widget=forms.RadioSelect)       
       

class DeleteAds(forms.Form):
    
    '''
    # The DeleteAds Class will display
    # form to delete internal & external ads.
    # Both internal & external will be 
    # dipslayed in checkboxes.  
    '''
    
    internalad_id = forms.ModelMultipleChoiceField(required=False, queryset=Internalad.objects.all(), widget=forms.CheckboxSelectMultiple)
    externalad_id = forms.ModelMultipleChoiceField(required=False, queryset=Externalad.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    
class EditInternalAd(forms.Form):
    
    '''
    # The EditInternalAd Class will display
    # form to Update internal ads by selecting 
    # internal ad displayed in combobox
    '''
    
    internalad_id = forms.ModelChoiceField(required=False, queryset=Internalad.objects.all(), label='Campaign Name')
    contentSpecific = forms.CharField(required=False, max_length=30, label='Content Specific')
    keywords = forms.CharField(required=False, max_length=30, label='Keywords')
    activeDate = forms.DateField(required=False, label='Active Date(mm/dd/yyyy)',  widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    expiredDate = forms.DateField(required=False, label='Expired Date(mm/dd/yyyy)', widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    noOfImpressions = forms.IntegerField(required=False, label='# of Impressions')
    priority = forms.IntegerField(required=False, label='Priority')
    maxImpressions = forms.IntegerField(required=False, label='Max. Impressions')
    targetpages = forms.CharField(required=False, label='Target Pages', widget=forms.Textarea)
    ad = forms.CharField(required=False, label='Ad', widget=forms.Textarea)
    adType = forms.ChoiceField(required=False, choices=[('Image','(300 x 250)'),
                                                        ('Banner1', '(160 x 600)'),
                                                        ('Banner2', '(728 x 90)')],
                                                        widget=forms.RadioSelect)
    myHiddenField = forms.BooleanField(widget = forms.HiddenInput(attrs={'id':'myHiddenFieldValue'}), required=False)  
    
class EditExternalAd(forms.Form):
    
    '''
    # The EditExternalAd Class will display
    # form to Update external ads by selecting 
    # external ad displayed in combobox
    '''
    
    externalad_id = forms.ModelChoiceField(required=False, queryset=Externalad.objects.all(), label='Campaign Name')
    adclient_id = forms.ModelChoiceField(widget = forms.Select(attrs={'id':'abc'}), required=False, queryset=Adclient.objects.all(), label='Client')
    contentSpecific = forms.CharField(required=False, max_length=30, label='Content Specific')
    keywords = forms.CharField(required=False, max_length=30, label='Keywords')
    activeDate = forms.DateField(required=False, label='Active Date',  widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    expiredDate = forms.DateField(required=False, label='Expired Date',  widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    noOfImpressions = forms.IntegerField(required=False, label='# of Impressions')
    priority = forms.IntegerField(required=False, label='Priority')
    maxImpressions = forms.IntegerField(required=False, label='Max. Impressions')
    targetPages = forms.CharField(required=False, label='Target Pages', widget=forms.Textarea)
    adCode = forms.CharField(required=False, max_length=30, label='Ad Code')
    ad = forms.CharField(required=False, label='Ad', widget=forms.Textarea)
    adType = forms.ChoiceField(required=False, choices=[('Image','(300 x 250)'),
                                                        ('Banner1', '(160 x 600)'),
                                                        ('Banner2', '(728 x 90)')],
                                                        widget=forms.RadioSelect)
    myHiddenField = forms.BooleanField(widget = forms.HiddenInput(attrs={'id':'myHiddenFieldValue'}), required=False)  