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

def execute(query,parameter=None,dictionary=False):
    ''' function for executing the query and retrieving data 
    return data type : list of tuple / list of dictionary'''

    conn=get_connection()
    if dictionary:
        cursor=conn.cursor(dictionary=True)
    else:
        cursor=conn.cursor()
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
        data=execute(query,parameter,dictionary=True)
        if data:
            return data[0]
        else:
            return None
    elif username:
        query='select * from users where username=%s'
        parameter=(username,)
        data=execute(query,parameter,dictionary=True)
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
    usernames=data #[d['username'] for d in data]
    return usernames

def delete_user(user_id):
    ''' Function for deleting user (account)
    args: user_id
    return: none'''

    query='delete from users where user_id= %s'
    parameter=(user_id,)
    data=execute(query,parameter)

def get_user_habits(user_id,active=True):
    '''function to get habits of a given user
    return: list of tuples'''

    query='select u.habit_id, h.habit_name from habits h join user_habits u on h.habit_id=u.habit_id where u.user_id=%s and is_active= %s'
    parameter=(user_id,active)
    data=execute(query,parameter)
    
    return data

def get_user_habit_info(user_id,habit_id):
    '''function to get info about habit a particular user have
    return : dictionary'''

    query='select * from user_habits where user_id =%s and habit_id =%s'
    parameter=(user_id,habit_id)
    data=execute(query,parameter,dictionary=True)
    return data[0]

def edit_user_habit(user_id,habit_id,frequency,goal):
    '''function to edit frequency and goal of a user habit'''

    query='update user_habits set frequency=%s,goal=%s where user_id =%s and habit_id=%s'
    parameters=(frequency,goal,user_id,habit_id)
    data=execute(query,parameters)

def end_user_habit(user_id,habit_id):
    '''function to end a user habit i.e. deactivating\discontinuing'''

    query='update user_habits set is_active=False,current_streak=0 where user_id =%s and habit_id=%s'
    parameters=(user_id,habit_id)
    data=execute(query,parameters)

def start_user_habit(user_id,habit_id):
    '''function to start a user habit i.e. activating\continuing'''

    query='update user_habits set is_active=True,current_streak=0 where user_id=%s and habit_id=%s'
    parameters=(user_id,habit_id)
    data=execute(query,parameters)

def get_other_habits(user_id):
    '''function to get habits other than the user have
    return type: list of tuples'''

    query='select habit_id ,habit_name from habits where habit_id not in (select habit_id from user_habits where user_id=%s)'
    parameter=(user_id,)
    data=execute(query,parameter)

    return data

def create_habit(habit_name,habit_description,points_per_day):
    '''Function to create a new habit'''

    query='insert into habits (habit_name,habit_description,points_per_day) values (%s,%s,%s)'
    parameters=(habit_name,habit_description,points_per_day)
    data = execute(query,parameters)



