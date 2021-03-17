# Some code sourced and modified from previous projects and assignments

import sys

def get_user_int(prompt, min, max):
    if max is None:
        return(get_user_int_no_max(prompt, min))
    while True:
        try:
            user_int = int(input(prompt))
            if min <= user_int and user_int <= max:
                return user_int
        except:
            pass
        print("Error: Invalid Input.")

def get_user_int_no_max(prompt, min):
    while True:
        try:
            user_int = int(input(prompt))
            if min <= user_int:
                return user_int
        except:
            pass
        print("Error: Invalid Input.")