import re
from django import forms
from django.core import validators

class login_form(forms.Form):
    Username = forms.CharField(widget = forms.TextInput(attrs={'class':'input_txt'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_txt'}))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'input_checkbox'}),
                                     required=False)
    
class signup_form(forms.Form):
    nickname = forms.CharField(widget = forms.TextInput(attrs={'class':'input_txt'}),
                               label="Username*", max_length=20,
                               validators=[ # custom validation
                                           validators.RegexValidator(regex=re.compile('^[A-Za-z0-9_\-\.]{6,20}$'), 
                                                                     code='invalid')
                                           ],
                               error_messages = { # custom error messages
                                                 'invalid': "Illegal characters in Username"
                                                 }
                               )
    
    #first_name = forms.CharField(label="First Name*", max_length=20)
    #last_name = forms.CharField(label="Last Name*", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_txt password'}),
                               label = "Password*", max_length=20,
                               validators=[ # custom validation
                                           validators.RegexValidator(regex=re.compile('^.{6,20}$'),
                                                                     code='invalid')
                                           ],
                               error_messages = { # custom error messages
                                                 'invalid': "Minimum 6 characters"
                                                 }
                               )
    
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input_txt '}), 
                                      label = "Repeat Password*", max_length=20,
                                      validators=[ # custom validation
                                                  validators.RegexValidator(regex=re.compile('^.{6,20}$'), 
                                                                             code='invalid')
                                                  ],
                                      error_messages = { # custom error messages
                                                        'invalid': "Minimum 6 characters"
    }
                                      )
    
    email = forms.EmailField(widget = forms.TextInput(attrs={'class':'input_txt'}))
    
    terms_agree = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'input_checkbox'}),
                                     required=False)
    
    #address = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':48}), label = "Residential Address*", max_length=200)
    #phone_number = forms.IntegerField(label="Phone Number*")
    #fax_number = forms.IntegerField(label="Fax Number", required = False)
    #website = forms.URLField(label="Website", required = False)