import string, random, uuid

from django.contrib.sessions.models import Session


def gen_rand_str(size = 10, chars = string.printable):
    """
     generates a string of random character from the given characterset
     with the givenstring length.
    """
    return ''.join(random.choice(chars) for x in range(size))

def gen_rand_obj(chars = [0,1,2,3,4,5,6,7,8,9]):
    '''
    generates a single random character from the given characterset.
    '''
    return random.choice(chars)

def is_userLogged(request):
    '''
     returns the user login status. returns True if a user is logged in,
     and False if no user is logged in.
    '''
    try:
        x = request.session['User_id']
        return True
    except KeyError:
        return False  

def isUserAction(request):
    '''
     @Author:Fouzia Riaz
     @Description:returns the action is set. returns True if an action is performed,
     and False if no action is performed.
    '''
    try:
        action = request.session['Action']
        if action:
            return True
    except KeyError:
        return False      
    