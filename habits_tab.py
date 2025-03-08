''' This module handles funtionality of habits tab'''

import tkinter as tk
from tkinter import ttk

import db

def habits_tab(dash,habits,user_instance):
    
    def get_habits(user_id):

        # retrieving habits of user
        return db.get_user_habits(user_id)

    # creating data frame
    data_frame=ttk.Frame(habits)
    data_frame.pack(expand=True,fill=tk.BOTH)

    # creating treeview to show habits data
    columns=['Habit_ID','Habit_Name','Description','Points_Per_Day','Goal','Frequency','Active']
    tree=ttk.Treeview(data_frame,columns=columns,show='headings')

    for col in columns:
        tree.heading(col,text=col)
        tree.column(col,width=100)

    data=get_habits(user_instance.user_id)

    for row in data:
        tree.insert('',tk.END,values=row)

    tree.pack(expand=True,fill=tk.BOTH)
        