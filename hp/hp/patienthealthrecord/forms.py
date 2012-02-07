from django import forms
from hp.patienthealthrecord.models import patienthealthrecord as Patienthealthrecord
from django.forms.widgets import Widget, Textarea
from django.forms.extras.widgets import SelectDateWidget
import datetime
    
class PatientHealthRecord(forms.Form):
    provincialHealthId = forms.CharField(label='Provincial Health ID')
    address = forms.CharField(label='Address')
    city = forms.CharField(label='City')
    province = forms.CharField(label='Province')
    postalCode = forms.CharField(label='Postal Code')
    dob = forms.DateField(widget=SelectDateWidget(years=range(1900, datetime.datetime.now().year + 1)), label='Date Of Birth')
    gender = forms.ChoiceField(choices=[('Not Specified', 'Not Specified'),
                                        ('Male','Male'),
                                        ('Female', 'Female')], label='Gender')


       

