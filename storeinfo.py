import sys
from getpass import getpass


def get_limit_number(limit_number):
    if limit_number == "":
        limit_number = 20
    elif limit_number.isdecimal():
        limit_number = int(limit_number)
    else:
        print("wrong format")
        sys.exit(1)
    return limit_number


def store_Id_Password(flags):
    user_info = {
            'userID': "",
            'password': ""
            }

    if not flags['userID'] and not flags['password']:
        user_info['userID'] = input('Please, input your userID:')
        user_info['password'] = getpass('Please, input your password:')
    elif not flags['userID'] and not flags['login_retry']:
        user_info['userID'] = input('Please, input your userID:')
    elif not flags['password'] and not flags['login_retry']:
        user_info['password'] = getpass('Please, input your password:')
    elif flags['login_retry']:
        user_info['userID'] = input('Please, input your userID:')
        user_info['password'] = getpass('Please, input your password:')
    else:
        user_info['userID'] = flags['userID']
        user_info['password'] = flags['password']

    return user_info
