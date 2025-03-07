''' Module for database connection and query function '''

import mysql.connector as m

def get_connection():
    ''' function for connecting to database habit_tracker
    returns connction object'''
    conn = m.connect(
        host="localhost",
        user="root",
        password="2830",
        database="Habit_Tracker",
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci"
    )
    return conn

def execute(query,parameter=None):
    ''' function for executing the query and retrieving data 
    return data type : list of dictionaries'''

    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute(query,parameter)
    data=cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return data

def get_user(user_id=None,username=None):
    ''' Function for getting user data 
    args: user_id (none) , username (none)
    return  : dictionary (user data)
            : none (no such user)'''
    
    if user_id:
        query='select * from users where user_id=%s'
        parameter=(user_id,)
        data=execute(query,parameter)
        if data:
            return data[0]
        else:
            return None
    elif username:
        query='select * from users where username=%s'
        parameter=(username,)
        data=execute(query,parameter)
        if data:
            return data[0]
        else:
            return None
    else:
        return None
    
def get_usernames():
    ''' Funtion to get list of usernames 
    return data type: list of usernames'''

    query='select username from users'
    data=execute(query)
    usernames=[d['username'] for d in data]
    return usernames

def delete_user(user_id):
    ''' Function for deleting user (account)
    args: user_id
    return: none'''

    query='delete from users where user_id= %s'
    parameter=(user_id,)
    data=execute(query,parameter)


