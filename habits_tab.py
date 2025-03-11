''' This module handles funtionality of habits tab'''

import tkinter as tk
from tkinter import ttk

import db

def habits_tab(dash,habits,user_instance):

    def display_info(event):
        index=habits_listbox.curselection()[0]
        if index >= len(user_habits):
            return
        
        selected_habit_id=user_habits[index][0]
        data=db.get_user_habit_info(user_id=user_instance.user_id,habit_id=selected_habit_id)
        v_habit_id.config(text=data['habit_id'])
        v_streak.config(text=data['current_streak'])
        v_habit.config(text=user_habits[index][1])
        v_freq.config(text=data['frequency'])
        v_goal.config(text=data['goal'])


    # styling
    style = ttk.Style()
    style.configure("Label.TLabel", font=("Arial", 10), foreground="black",background='light grey')
    style.configure("Info.TLabel", font=("Arial", 10), foreground="dark green",background='light grey')

    # creating frame for menubutton
    options_frame=ttk.Frame(habits)
    options_frame.pack(fill='x')

    # creating a menubutton
    options=ttk.Menubutton(options_frame,text='More Options')
    options.pack(padx=20,pady=10,side='right')

    #creating menu
    menu=tk.Menu(options,tearoff=0)
    menu.add_command(label='Continue existing Habit',command= lambda : print('success '))
    menu.add_separator()
    menu.add_command(label='Create New Habit',command= lambda : print('success'))
    menu.add_separator()
    menu.add_command(label='Delete Habit',command= lambda : print('success '))
    options.config(menu=menu)
    
    ###
    # creating display frame
    display_frame=ttk.Frame(habits)
    display_frame.pack(expand=True,fill=tk.BOTH)
    
    # creating info frame
    info_frame=ttk.Frame(display_frame,style='test.TFrame')
    info_frame.pack(side=tk.LEFT,fill='y')
    
    # creating lable that acts as headings
    headings=ttk.Label(info_frame,text='ID : Habit Name')
    headings.pack(padx=20,fill='x')

    # creatinf a listbox for user habits
    habits_listbox=tk.Listbox(info_frame,selectmode=tk.SINGLE,bd=2,relief=tk.SUNKEN)
    habits_listbox.pack(padx=20,pady=10,fill=tk.BOTH,side='left')
    habits_listbox.bind('<<ListboxSelect>>', display_info)

    # creating scrollbar for listbox
    scrollbar=ttk.Scrollbar(info_frame,orient=tk.VERTICAL,command=habits_listbox.yview)
    scrollbar.pack(side='left',fill='y')
    
    # linking scrollbar to listbox
    habits_listbox.config(yscrollcommand=scrollbar.set)

    # populating habits_list
    user_habits=db.get_user_habits(user_instance.user_id)
    for habit_id,habit_name in user_habits:
        habits_listbox.insert(tk.END,f'{habit_id} : {habit_name}')

    ### creating action frame
    action_frame=ttk.Frame(display_frame,style="test.TFrame")
    action_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

    # Row 0 habit id and current streak (test)
    l_habit_id=ttk.Label(action_frame,text='Habit ID :',style='Label.TLabel')
    l_habit_id.grid(row=0,column=0,padx=10,pady=(30,5),sticky='w')
    v_habit_id=ttk.Label(action_frame,text='',style='Info.TLabel')
    v_habit_id.grid(row=0,column=1,padx=10,pady=(30,5),sticky='w')

    l_streak=ttk.Label(action_frame,text='Current Streak :',style='Label.TLabel')
    l_streak.grid(row=0,column=2,padx=10,pady=(30,5),sticky='w')
    v_streak=ttk.Label(action_frame,text='',style='Info.TLabel')
    v_streak.grid(row=0,column=3,padx=10,pady=(30,5),sticky='w')

    # Row 1 habit name
    l_habit=ttk.Label(action_frame,text='Habit Name :',style='Label.TLabel')
    l_habit.grid(row=1,column=0,columnspan=2,padx=10,pady=5,sticky='w')
    v_habit=ttk.Label(action_frame,text='',style='Info.TLabel')
    v_habit.grid(row=1,column=2,columnspan=2,padx=10,pady=5,sticky='w')

    # Row 2 frequency
    l_freq=ttk.Label(action_frame,text='Frequency :',style='Label.TLabel')
    l_freq.grid(row=2,column=0,columnspan=2,padx=10,pady=5,sticky='w')
    v_freq=ttk.Label(action_frame,text='',style='Info.TLabel')
    v_freq.grid(row=2,column=2,columnspan=2,padx=10,pady=5,sticky='w')

    # Row 3 goal 
    l_goal=ttk.Label(action_frame,text='Goal :',style='Label.TLabel')
    l_goal.grid(row=3,column=0,columnspan=2,padx=10,pady=5,sticky='w')
    # Row 4 goal val
    v_goal=tk.Message(action_frame,text='',width=250,bg='light grey',fg='dark green')
    v_goal.grid(row=3,column=2,columnspan=3,padx=10,pady=5,sticky='w')

