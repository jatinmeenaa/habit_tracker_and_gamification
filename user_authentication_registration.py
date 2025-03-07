''' Module for user authentication and management '''

import bcrypt
import re

import db

def email_exists(email):
    ''' Checks if the email exists for new users'''

    query="SELECT * FROM users WHERE email=%s"
    parameter=(email,)
    data=db.execute(query,parameter) 
    if data:
        return True
    else:
        return False
    
def username_exists(username):
    ''' Checks if the username taken'''

    query="SELECT * FROM users WHERE username=%s"
    parameter=(username,)
    data=db.execute(query,parameter) 
    if data:
        return True
    else:
        return False

def is_user_authentic(username,password):
    ''' Checks if the user is authentic 
    True: if user credentials are valid
    False: either username doesn't exist or wrong password'''
    
    query='select password_hash from users where username=%s'
    parameter=(username,)
    data=db.execute(query,parameter)
    if data:
        password_hash=data[0]['password_hash']
        if bcrypt.checkpw(password.encode(),password_hash.encode()):
            return True
        else :
            return False
    else:
        return False
    
def register_user(email,username,password):
    '''Inserts the data of newly registered user'''

    password_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    query='insert into users (email,username,password_hash) values (%s, %s, %s)'
    parameters=(email,username,password_hash)
    data=db.execute(query,parameters)

def is_email_valid(email):
    pattern = r"^(?!.*\.\.)[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if bool(re.match(pattern, email)):
        return True
    else:
        return False

def is_username_valid(username):
    pattern=r'^[A-Za-z0-9_]{5,}$'
    if bool(re.match(pattern,username)):
        return True
    else :
        return False

def is_valid_and_strong(password):
    pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!])[A-Za-z\d@#$%^&+=!]{8,}$'
    if bool(re.match(pattern,password)):
        return True
    else:
        return False
    
def change_user_password(password,user_id):
    '''Changes password'''

    password_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    query='update users set password_hash=%s where user_id = %s'
    parameters=(password_hash,user_id)
    data=db.execute(query,parameters)

def update_username(username,user_id):
    query='update users set username= %s where user_id = %s'
    parameters=(username,user_id)
    data=db.execute(query,parameters)

def update_email(email,user_id):
    query='update users set email= %s where user_id = %s'
    parameters=(email,user_id)
    data=db.execute(query,parameters)
    





