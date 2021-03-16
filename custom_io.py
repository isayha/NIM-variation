# Some code sourced and modified from previous projects and assignments

import sys

def get_user_int(prompt):
    try:
        return(int(input(prompt)))
    except:
        return(None)