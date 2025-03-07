''' Module for user class'''

import db

class User():
    ''' Stores user info upon successful login '''

    def __init__(self,user_id,username,email,total_points):
        self.user_id=user_id
        self.username=username
        self.email=email
        self.total_points=total_points
    

def create_user(username):
    data=db.get_user(username=username)
    user=User(data['user_id'],data['username'],data['email'],data['total_points'])
    return user