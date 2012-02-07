import hashlib,datetime

from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect

from django.template import RequestContext

from django.db.models import Q

from django.conf import settings

from hp.user.forms import login_form, signup_form

from hp.user.models import user as User

from hp.hp_utils import gen_rand_str, is_userLogged


def logout(request):
    try:
        del request.session['User_id']
    except:
        pass
    request.session.flush()
    request.session.set_expiry((datetime.datetime.now() + datetime.timedelta(seconds = 2)))
    return HttpResponseRedirect('/')


def login(request):
    if request.method == "POST":
        loginform = login_form(request.POST)
        if loginform.is_valid():
            clean_data = loginform.cleaned_data
            
            # Retrieve user object from databse, catch exception if matching object
            # does not exist.
            
            try:
                get_user = User.objects.get(Q(nickname = clean_data['Username']) | Q(email = clean_data['Username']))
            except User.DoesNotExist:
                
                # noUser tag used by template to display error message.
            
                return render_to_response('sign_in.html',
                                          {'loginform':loginform, 'noUser': True}, 
                                          context_instance=RequestContext(request))
            
            # Generate hash and match User Password.
            
            if get_user:
                try:
                    if hashlib.sha256(get_user.pw_salt + 
                                      clean_data['Password']).hexdigest() == get_user.password:
                        request.session.flush()
                        if clean_data['remember_me']:
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                            request.session.set_expiry((datetime.datetime.now() + datetime.timedelta(hours = 336)))
                        else:
                            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                            request.session.set_expiry((datetime.datetime.now() + datetime.timedelta(hours = 6)))
                            
                        request.session['User_id'] = get_user.id
                        redirect_to = request.REQUEST.get('next', '')
                        if redirect_to:
                            return HttpResponseRedirect(redirect_to)
                        else:
                            return HttpResponseRedirect('/refresh_page/')
                    
                except:
                    return render_to_response('sign_in.html',
                                              {'loginform':loginform, 'badPw': True}, 
                                              context_instance=RequestContext(request))
                else:
                    
                    # noUser tag used by template to display error message.  

                    return render_to_response('sign_in.html',
                                              {'loginform':loginform, 'badPw': True}, 
                                              context_instance=RequestContext(request))
    
    # If method not POST return blank login form.
    
    else:
        loginform = login_form()
    return render_to_response('sign_in.html',{'loginform':loginform}, 
                              context_instance=RequestContext(request))
        

def signup(request):
    if not is_userLogged(request):
        
        if request.method == "POST":
            signupform = signup_form(request.POST)
            if signupform.is_valid():
                clean_data = signupform.cleaned_data
                
                # Check if a User already exists by the given username.   
                try:
                    get_user = User.objects.get(nickname = clean_data['nickname'])
                    
                    # If username found display error
                    
                    if get_user:
                        return render_to_response('sign_up.html', 
                                                  {'signupform':signupform, 'userExists': True}, 
                                                  context_instance=RequestContext(request))
    
                # If no user found, match passwords and create new user
                
                except User.DoesNotExist:
                    pass
                
                try:
                    get_email_user = User.objects.get(email = clean_data['email'])                    
                    if get_email_user:
                        return render_to_response('sign_up.html', 
                                                  {'signupform':signupform, 'emailExists': True}, 
                                                  context_instance=RequestContext(request))
                        
                except User.DoesNotExist:
                    if clean_data['password'] != clean_data['repeat_password']:
                        return render_to_response('sign_up.html',
                                                   {'signupform':signupform, 'passwordMismatch' : True}, 
                                                   context_instance=RequestContext(request))
                        
                    if not clean_data['terms_agree']:
                        return render_to_response('sign_up.html',
                                                   {'signupform':signupform, 'terms_error' : True}, 
                                                   context_instance=RequestContext(request))
                        
                               
                    # Generate a random user salt
                    user_salt = gen_rand_str()
                    
                    # Generate hash for user password
                    pw_hash = hashlib.sha256(user_salt + clean_data['password']).hexdigest()
                    
                    new_user = User(nickname = clean_data['nickname'],
                                    #first_name = clean_data['first_name'],
                                    #last_name = clean_data['last_name'],
                                    password = pw_hash,
                                    pw_salt = user_salt,
                                    email = clean_data['email'],
                                    join_date_time = datetime.datetime.now()
                                    #address = clean_data['address'],
                                    #phone_number = clean_data['phone_number'],
                                    #fax_number = clean_data['fax_number'],
                                    #website = clean_data['website'] 
                                    )
                    
                    # Try to save new user to Databse. return userCreateError if unable
                    # to save user to databse, due to any reason.
                    
                    try:
                        new_user.save()
                        
                        get_user = User.objects.get(nickname = clean_data['nickname'])
                        request.session.flush()
                        request.session['User_id'] = get_user.id
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                        request.session.set_expiry((datetime.datetime.now() + datetime.timedelta(hours = 6)))
                        return HttpResponseRedirect('/refresh_page/')
                    
                    except:
                        return render_to_response('sign_up.html', 
                                                  {'signupform':signupform, 'userCreateError': True}, 
                                                  context_instance=RequestContext(request))
                        
        # If method not POST return blank signup form.
                        
        else:
            signupform = signup_form()
        return render_to_response('sign_up.html', 
                                  {'signupform':signupform, 'start' : True}, 
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/refresh_page/')




