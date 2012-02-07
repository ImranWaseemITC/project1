from django import forms
from django.forms.widgets import Widget, Textarea



class CreatePersonalProfile(forms.Form):
    
    myHiddenField = forms.CharField(widget = forms.HiddenInput(), required=False)
    profileName = forms.CharField()
    firstName = forms.CharField()
    middleName = forms.CharField()
    lastName = forms.CharField()
    dob = forms.DateField(widget=forms.DateInput(attrs={'id':'mydatefield'})) 
    sex = forms.ChoiceField(choices=[('Male','Male'),
                                   ('Female', 'Female'),
                                   ("I'd rather not say", "I'd rather not say")],
                                     widget=forms.Select(attrs={'class':'small_select'}))
    bloodType = forms.CharField()
    ethinicity = forms.CharField()
    
class CreatePersonalProfile_Phone(forms.Form):
    phone = forms.IntegerField()
    phoneType = forms.CharField()
    
class CreatePersonalProfile_Email(forms.Form):
    email = forms.EmailField()
    emailType = forms.CharField()
    
class CreatePersonalProfile_Adress(forms.Form):
    adress = forms.CharField()
    adressType = forms.CharField()
    
class CreateSocialHistory(forms.Form):
    
    myHiddenField = forms.CharField(widget = forms.HiddenInput(), required=False)
    maritalStatus = forms.ChoiceField(choices=[('Married','Married'),
                                             ('Never married', 'Never married'),
                                             ('Single, formerly married', 'Single, formerly married'),
                                             ('Common Law', 'Common Law')],
                                             widget=forms.Select(attrs={'class':'small_select'}))
    workConditions = forms.CharField(widget=forms.Textarea)
    drugUse = forms.CharField(widget=forms.Textarea)
    physicalActivity = forms.CharField(widget=forms.Textarea)
    
class CreateEmergencyContacts(forms.Form):
    
    myHiddenField1 = forms.CharField(widget = forms.HiddenInput(), required=False)
    myHiddenField2 = forms.CharField(widget = forms.HiddenInput(), required=False)
    firstName = forms.CharField()
    middleName = forms.CharField()
    lastName = forms.CharField()
    relationship = forms.CharField()     
    
class CreateEmergencyContacts_Phone(forms.Form):
    
    phone = forms.IntegerField()
    phoneType = forms.CharField()
    
class CreateEmergencyContacts_Email(forms.Form):
    
    email = forms.EmailField()
    emailType = forms.CharField()
    
class CreateEmergencyContacts_Adress(forms.Form):
    
    adress = forms.CharField()
    adressType = forms.CharField()
    
class CreateFamilyHistory(forms.Form):
    
    myHiddenField1 = forms.CharField(widget = forms.HiddenInput(), required=False)
    myHiddenField2 = forms.CharField(widget = forms.HiddenInput(), required=False)
    condition = forms.CharField()
    relation = forms.CharField()
    relationshipType = forms.ChoiceField(choices=[('Maternal','Maternal'),
                                                ('Paternal', 'Paternal')],
                                                 widget=forms.Select(attrs={'class':'small_select'}))
    period = forms.CharField()
    gender = forms.ChoiceField(choices=[('Male','Male'),
                                   ('Female', 'Female'),
                                   ("I'd rather not say", "I'd rather not say")],
                                     widget=forms.Select(attrs={'class':'small_select'}))

