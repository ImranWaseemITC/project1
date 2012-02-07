"""
# Product: Health Park Business Solution
# Copyright (C) 2011-2012 Health Park, Inc. All Rights Reserved.
# 
# info@healthpark.ca or http://www.healthpark.ca/license.html
"""
from django import template

register = template.Library()

@register.filter()
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)
    mult.is_safe = False
    
@register.filter()
def is_greater_than(value, arg):
    if str(type(value)) == "<type 'int'>":
        if value > arg:
            return True
    elif len(value) > arg:
        return True
    else:
        return False