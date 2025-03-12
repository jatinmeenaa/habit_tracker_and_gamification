''' This module handles funtionality of habits tab'''

import tkinter as tk
from tkinter import ttk

import db

def habits_tab(dash,habits,user_instance):

    def display_info(event):
        index=habits_listbox.curselection()[0]
        if index >= len(user_active_habits):
            return
        
        selected_habit_id=user_active_habits[index][0]
        data=db.get_user_habit_info(user_id=user_instance.user_id,habit_id=selected_habit_id)
        v_habit_id.config(text=data['habit_id'])
        v_streak.config(text=data['current_streak'])
        v_habit.config(text=user_active_habits[index][1])
        v_freq.config(text=data['frequency'])
        v_goal.config(text=data['goal'])

        edit_button.grid(row=5,column=0,padx=10,pady=5,sticky='w')
        if guide_label.cget('text')=='Active Habits':
            end_button.grid(row=6,column=0,padx=10,pady=5,sticky='w')
        elif guide_label.cget('text')=='Inactive Habits':
            start_button.grid(row=6,column=0,padx=10,pady=5,sticky='w')

    def populate_habits(habits):
        habits_listbox.delete(0,tk.END)
        for habit_id,habit_name in habits:
            habits_listbox.insert(tk.END,f'{habit_id} : {habit_name}')

    def edit_habit():
        edit_button.grid_forget()
        end_button.grid_forget()
        start_button.grid_forget()
        v_freq.grid_forget()
        v_goal.grid_forget()
        info_frame.pack_forget()
        edit_freq.grid(row=2,column=2,columnspan=2,padx=10,pady=5,sticky='w')
        edit_freq.config(text=v_freq.cget('text'))
        edit_goal.grid(row=3,column=2,columnspan=3,padx=10,pady=5,sticky='w')
        edit_goal.delete('1.0',tk.END)
        edit_goal.insert(tk.END,v_goal.cget('text'))
        save_button.grid(row=5,column=0,padx=10,pady=5,sticky='w')
        cancel_button.grid(row=5,column=2,padx=10,pady=5,sticky='w')

    def end_habit():
        db.end_user_habit(user_instance.user_id,v_habit_id.cget('text'))
        index=habits_listbox.curselection()[0]
        habits_listbox.delete(index)
        user_active_habits.pop(index)

        v_habit_id.config(text='')
        v_streak.config(text='')
        v_habit.config(text='')
        v_freq.config(text='')
        v_goal.config(text='')
        edit_button.grid_forget()
        end_button.grid_forget()

    def cancel_edit():
        edit_button.grid(row=5,column=0,padx=10,pady=5,sticky='w')
        if guide_label.cget('text')=='Active Habits':
            end_button.grid(row=6,column=0,padx=10,pady=5,sticky='w')
        elif guide_label.cget('text')=='Inactive Habits':
            start_button.grid(row=6,column=0,padx=10,pady=5,sticky='w')
        v_freq.grid(row=2,column=2,columnspan=2,padx=10,pady=5,sticky='w')
        v_goal.grid(row=3,column=2,columnspan=3,padx=10,pady=5,sticky='w')
        info_frame.pack(side=tk.LEFT,fill='y')
        action_frame.pack_forget()
        action_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        edit_freq.grid_forget()
        edit_freq.config(text=v_freq.cget('text'))
        edit_goal.grid_forget()
        edit_goal.insert(tk.END,v_goal.cget('text'))
        save_button.grid_forget()
        cancel_button.grid_forget()

    def save_edit():
        db.edit_user_habit(user_instance.user_id,v_habit_id.cget('text'),edit_freq.cget('text'),edit_goal.get("1.0", "end-1c"))
        v_freq.config(text=edit_freq.cget('text'))
        v_goal.config(text=edit_goal.get("1.0", "end-1c"))
        cancel_edit()

    def continue_habit():
        inactive_habits=db.get_user_habits(user_instance.user_id,active=False)
        guide_label.config(text='Inactive Habits')
        populate_habits(inactive_habits)

        v_habit_id.config(text='')
        v_streak.config(text='')
        v_habit.config(text='')
        v_freq.config(text='')
        v_goal.config(text='')
        edit_button.grid_forget()
        end_button.grid_forget()

    def start_habit():
        print(user_instance.user_id,v_habit_id.cget('text'))
        db.start_user_habit(user_instance.user_id,v_habit_id.cget('text'))
        
        index=habits_listbox.curselection()[0]
        habits_listbox.delete(index)
        user_inactive_habits.pop(index)

        v_habit_id.config(text='')
        v_streak.config(text='')
        v_habit.config(text='')
        v_freq.config(text='')
        v_goal.config(text='')
        edit_button.grid_forget()
        start_button.grid_forget()


    # styling
    style = ttk.Style()
    style.configure("Label.TLabel", font=("Arial", 10), foreground="black",background='light grey')
    style.configure("Info.TLabel", font=("Arial", 10), foreground="dark green",background='light grey')

    # creating frame for menubutton
    options_frame=ttk.Frame(habits)
    options_frame.pack(fill='x')

    # creating guiding label
    guide_label=ttk.Label(options_frame,text='Active Habits')
    guide_label.pack(padx=20,pady=10,side='left')

    # creating a menubutton
    options=ttk.Menubutton(options_frame,text='More Options')
    options.pack(padx=20,pady=10,side='right')

    #creating menu
    menu=tk.Menu(options,tearoff=0)
    menu.add_command(label='Continue existing Habit',command= continue_habit)
    menu.add_separator()
    menu.add_command(label='Start a Habit',command= lambda : print('success'))
    menu.add_separator()
    menu.add_command(label='Create New Habit',command= lambda : print('success '))
    options.config(menu=menu)

    
    ###
    # creating display frame
    display_frame=ttk.Frame(habits)
    display_frame.pack(expand=True,fill=tk.BOTH)
    
    # creating info frame
    info_frame=ttk.Frame(display_frame)
    info_frame.pack(side=tk.LEFT,fill='y')
    
    # creating lable that acts as headings
    headings=ttk.Label(info_frame,text='ID : Habit Name')
    headings.pack(padx=20,fill='x')

    # creating a listbox for habits display
    habits_listbox=tk.Listbox(info_frame,selectmode=tk.SINGLE,bd=2,relief=tk.SUNKEN)
    habits_listbox.pack(padx=20,pady=10,fill=tk.BOTH,side='left')
    habits_listbox.bind('<<ListboxSelect>>', display_info)

    # creating scrollbar for listbox
    scrollbar=ttk.Scrollbar(info_frame,orient=tk.VERTICAL,command=habits_listbox.yview)
    scrollbar.pack(side='left',fill='y')
    
    # linking scrollbar to listbox
    habits_listbox.config(yscrollcommand=scrollbar.set)

    # poputating active habits
    user_active_habits=db.get_user_habits(user_instance.user_id)
    user_inactive_habits=db.get_user_habits(user_instance.user_id,False)
    populate_habits(user_active_habits)

    ### creating action frame
    action_frame=ttk.Frame(display_frame)
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

    # Row 2 frequency | edit frequency
    l_freq=ttk.Label(action_frame,text='Frequency :',style='Label.TLabel')
    l_freq.grid(row=2,column=0,columnspan=2,padx=10,pady=5,sticky='w')
    v_freq=ttk.Label(action_frame,text='',style='Info.TLabel')
    v_freq.grid(row=2,column=2,columnspan=2,padx=10,pady=5,sticky='w')

    edit_freq=ttk.Menubutton(action_frame)
    edit_freq.grid_forget()
    menu_freq=tk.Menu(edit_freq,tearoff=0)
    menu_freq.add_command(label='daily',command= lambda : edit_freq.config(text='daily'))
    menu_freq.add_separator()
    menu_freq.add_command(label='weekly',command= lambda : edit_freq.config(text='weekly'))
    menu_freq.add_separator()
    menu_freq.add_command(label='monthly',command= lambda : edit_freq.config(text='monthly'))
    edit_freq.config(menu=menu_freq)


    # Row 3 goal 
    l_goal=ttk.Label(action_frame,text='Goal :',style='Label.TLabel')
    l_goal.grid(row=3,column=0,columnspan=2,padx=10,pady=5,sticky='w')
    # Row 4 goal val | edit goal
    v_goal=tk.Message(action_frame,text='',width=250,bg='light grey',fg='dark green')
    v_goal.grid(row=3,column=2,columnspan=3,padx=10,pady=5,sticky='w')

    edit_goal=tk.Text(action_frame,width=25,height=4)
    edit_goal.grid_forget()

    # Row 5 edit button | save button | cancel button
    edit_button=ttk.Button(action_frame,text='Edit',command=edit_habit)
    edit_button.grid_forget()

    start_button=ttk.Button(action_frame,text='Start',command=start_habit)
    start_button.grid_forget()

    save_button=ttk.Button(action_frame,text='Save', command=save_edit)
    save_button.grid_forget()

    cancel_button=ttk.Button(action_frame,text='Cancel',command= cancel_edit)
    cancel_button.grid_forget()

    # Row 6 end button
    end_button=ttk.Button(action_frame,text='End',command=end_habit)
    end_button.grid_forget()



