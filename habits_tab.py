''' This module handles funtionality of habits tab'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import db

def habits_tab(dash,habits,user_instance):

    def show_user_habits():
        '''Modify tab to show user active habits'''

        def action_on_selection(event):
            display_info(user_active_habits)
            # action buttons
            edit_button.grid(row=5,column=0,padx=10,pady=5,sticky='w')
            end_button.grid(row=6,column=0,padx=10,pady=5,sticky='w')
        
        # modify layout
        create_habit_frame.pack_forget()
        start_habit_frame.pack_forget()
        info_frame.pack(side=tk.LEFT,fill='y')
        action_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        # guide label
        guide_label.config(text='Show User Habits')
        # poputating active habits
        global user_active_habits
        user_active_habits=db.get_user_habits(user_instance.user_id)
        populate_habits(user_active_habits)
        # action when any habit selected
        habits_listbox.bind('<<ListboxSelect>>',action_on_selection)

    def continue_habits():
        '''Modify tab to show inactive habits to continue again'''

        def action_on_selection(event):
            display_info(user_inactive_habits)
            # action buttons
            edit_button.grid(row=5,column=0,padx=10,pady=5,sticky='w')
            start_button.grid(row=6,column=0,padx=10,pady=5,sticky='w')
        
        # modify layout
        create_habit_frame.pack_forget()
        start_habit_frame.pack_forget()
        info_frame.pack(side=tk.LEFT,fill='y')
        action_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        # guide label
        guide_label.config(text='Continue Inactive Habits')
        # populating inactive habits
        global user_inactive_habits
        user_inactive_habits=db.get_user_habits(user_instance.user_id,False)
        populate_habits(user_inactive_habits)
        # action on habit selection
        habits_listbox.bind('<<ListboxSelect>>',action_on_selection)

    def start_habits():
        '''Modify tab to show habits to add it to user habits'''
        
        def action_on_selection(event):
            index=habits_listbox.curselection()[0]
            habit_id=other_habits[index][0]
            data=db.get_habit_info(habit_id)
            # displaying the selected 
            start_habit_n.config(text=data['habit_name'])
            start_habit_d.config(text=data['habit_description'])


        # modify layout
        create_habit_frame.pack_forget()
        action_frame.pack_forget()
        info_frame.pack(side=tk.LEFT,fill='y')
        start_habit_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        # guide label
        guide_label.config(text='Start New Habit')
        # populating inactive habits
        global other_habits
        other_habits=db.get_other_habits(user_instance.user_id)
        populate_habits(other_habits)
        # action on habit selection
        habits_listbox.bind('<<ListboxSelect>>',action_on_selection)

    def create_habits():
        '''Modify tab to create new habits to add it to user habits later'''
        
        # modify layout
        info_frame.pack_forget()
        action_frame.pack_forget()
        start_habit_frame.pack_forget()
        create_habit_frame.pack(fill=tk.BOTH,expand=True)

        # guide label
        guide_label.config(text='Create New Habit')

    def display_info(habit_list):
        index=habits_listbox.curselection()[0]
        if index >= len(habit_list):
            return
        
        selected_habit_id=habit_list[index][0]
        data=db.get_user_habit_info(user_id=user_instance.user_id,habit_id=selected_habit_id)
        v_habit_id.config(text=data['habit_id'])
        v_streak.config(text=data['current_streak'])
        v_habit.config(text=habit_list[index][1])
        v_freq.config(text=data['frequency'])
        v_goal.config(text=data['goal'])

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
        if guide_label.cget('text')=='Show Active Habits':
            end_button.grid(row=6,column=0,padx=10,pady=5,sticky='w')
        elif guide_label.cget('text')=='Continue Inactive Habits':
            start_button.grid(row=6,column=0,padx=10,pady=5,sticky='w')
        v_freq.grid(row=2,column=2,columnspan=2,padx=10,pady=5,sticky='w')
        v_goal.grid(row=3,column=2,columnspan=3,padx=10,pady=5,sticky='w')
        info_frame.pack(side=tk.LEFT,fill='y')
        action_frame.pack_forget()
        action_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        edit_freq.grid_forget()
        #edit_freq.config(text=v_freq.cget('text'))
        edit_goal.grid_forget()
        #edit_goal.insert(tk.END,v_goal.cget('text'))
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
        end_button.grid_forget()

    def clear_habit_create():
        habit_n_entry.delete(0,tk.END)
        habit_d_text.delete('1.0',tk.END)
        points_entry.delete(0,tk.END)
        points_entry.insert(tk.END,'10')

    def create_habit_create():
        '''command function for create button'''

        habit_name=habit_n_entry.get().strip()
        habit_description=habit_d_text.get('1.0',tk.END).strip()
        points_per_day=points_entry.get().strip()
        # error if no type matching
        db.create_habit(habit_name,habit_description,points_per_day)
        messagebox.showinfo('Habit Created Successfully',f'New Habit {habit_name} created successfully')
        clear_habit_create()

    def start_new_habit():
        if habits_listbox.curselection():
            index=habits_listbox.curselection()[0]
            habit_id=other_habits[index][0]
            frequency=start_habit_f_mb.cget('text')
            goal=start_habit_g.get('1.0',tk.END).strip()
            db.start_new_user_habit(user_instance.user_id,habit_id,goal,frequency)
            habits_listbox.delete(index)
            other_habits.pop(index)
            cancel_start_new_habit()

    def cancel_start_new_habit():
        habits_listbox.selection_clear(0,tk.END)
        start_habit_n.config(text='')
        start_habit_d.config(text='')
        start_habit_g.delete('1.0',tk.END)
        start_habit_f_mb.config(text='daily')

    # styling
    style = ttk.Style()
    style.configure("Label.TLabel", font=("Arial", 10), foreground="black",background='light grey')
    style.configure("Info.TLabel", font=("Arial", 10), foreground="dark green",background='light grey')

    # creating frame for menubutton
    options_frame=ttk.Frame(habits)
    options_frame.pack(fill='x')

    # creating guiding label
    guide_label=ttk.Label(options_frame,text='')
    guide_label.pack(padx=20,pady=10,side='left')

    # creating a menubutton
    options=ttk.Menubutton(options_frame,text='More Options')
    options.pack(padx=20,pady=10,side='right')

    #creating menu
    menu=tk.Menu(options,tearoff=0)
    menu.add_command(label='Show User Habits',command= show_user_habits)
    menu.add_separator()
    menu.add_command(label='Continue existing Habit',command= continue_habits)
    menu.add_separator()
    menu.add_command(label='Start a Habit',command= start_habits)
    menu.add_separator()
    menu.add_command(label='Create New Habit',command= create_habits)
    options.config(menu=menu)

    
    ###
    # creating display frame
    display_frame=ttk.Frame(habits)
    display_frame.pack(expand=True,fill=tk.BOTH)
    
    ## creating create habit frame
    create_habit_frame=ttk.Frame(display_frame)
    create_habit_frame.pack_forget()

    # Row 0 habitname
    habit_n_label=ttk.Label(create_habit_frame,text='Habit Name :',style='Label.TLabel')
    habit_n_label.grid(row=0,column=0,padx=10,pady=(30,5),sticky='w')
    habit_n_entry=ttk.Entry(create_habit_frame,state='Info.TEntry')
    habit_n_entry.grid(row=0,column=1,padx=10,pady=(30,5),sticky='w')

    # Row 1 description
    habit_d_label=ttk.Label(create_habit_frame,text='Habit Description :',style='Label.TLabel')
    habit_d_label.grid(row=1,column=0,padx=10,pady=5,sticky='w')
    habit_d_text=tk.Text(create_habit_frame,width=50,height=4)
    habit_d_text.grid(row=1,column=1,padx=10,pady=5,sticky='w')

    # Row 2 points per day
    points_label=ttk.Label(create_habit_frame,text='Points Per Day :',style='Label.TLabel')
    points_label.grid(row=2,column=0,padx=10,pady=5,sticky='w')
    points_entry=ttk.Entry(create_habit_frame,style='Info.TEntry')
    points_entry.grid(row=2,column=1,padx=10,pady=5,sticky='w')
    points_entry.insert(tk.END,'10')

    # Row 3 create button | clear button
    create_button=ttk.Button(create_habit_frame,text='Create',command=create_habit_create)
    create_button.grid(row=3,column=0,padx=10,pady=(10,5),sticky='w')

    clear_button=ttk.Button(create_habit_frame,text='Clear',command=clear_habit_create)
    clear_button.grid(row=3,column=1,padx=10,pady=(10,5),sticky='w')

    ## creating start habit frame
    start_habit_frame=ttk.Frame(display_frame)
    start_habit_frame.pack_forget()

    # Row 0 habit_name
    start_habit_n_label=ttk.Label(start_habit_frame,text='Habit Name :',style='Label.TLabel')
    start_habit_n_label.grid(row=0,column=0,padx=10,pady=(30,5),sticky='w')
    start_habit_n=ttk.Label(start_habit_frame,text='',style='Info.TLabel')
    start_habit_n.grid(row=0,column=1,padx=10,pady=(30,5),sticky='w')

    # Row 1 habit_description
    start_habit_d_label=ttk.Label(start_habit_frame,text='Description :',style='Label.TLabel')
    start_habit_d_label.grid(row=1,column=0,padx=10,pady=5,sticky='w')
    start_habit_d=tk.Message(start_habit_frame,text='',background='light grey',foreground='dark green',width=300,font=('Arial',11))
    start_habit_d.grid(row=1,column=1,padx=10,pady=5,sticky='w')

    # Row 2 goal
    start_habit_g_label=ttk.Label(start_habit_frame,text='Goal :',style='Label.TLabel')
    start_habit_g_label.grid(row=2,column=0,padx=10,pady=5,sticky='w')
    start_habit_g=tk.Text(start_habit_frame,height=4,width=30,wrap='word')
    start_habit_g.grid(row=2,column=1,padx=10,pady=5,sticky='w')

    # Row 3 frequency
    start_habit_f_label=ttk.Label(start_habit_frame,text='Frequency :',style='Label.TLabel')
    start_habit_f_label.grid(row=3,column=0,padx=10,pady=5,sticky='w')
    start_habit_f_mb=ttk.Menubutton(start_habit_frame,text='daily')
    start_habit_f_mb.grid(row=3,column=1,padx=10,pady=5,sticky='w')
    start_habit_f_menu=tk.Menu(start_habit_f_mb,tearoff=0)
    start_habit_f_menu.add_command(label='daily',command=lambda : start_habit_f_mb.config(text='daily'))
    start_habit_f_menu.add_separator()
    start_habit_f_menu.add_command(label='weekly',command=lambda : start_habit_f_mb.config(text='weekly'))
    start_habit_f_menu.add_separator()
    start_habit_f_menu.add_command(label='monthly',command=lambda : start_habit_f_mb.config(text='monthly'))
    start_habit_f_mb.config(menu=start_habit_f_menu)

    # Row 4 start button | cancel button
    start_habit_start_b=ttk.Button(start_habit_frame,text='Start',command=start_new_habit)
    start_habit_start_b.grid(row=4,column=0,padx=10,pady=10,sticky='w')
    
    start_habit_cancel_b=ttk.Button(start_habit_frame,text='Cancel',command=cancel_start_new_habit)
    start_habit_cancel_b.grid(row=4,column=1,padx=10,pady=10,sticky='w')


    ## creating info frame
    info_frame=ttk.Frame(display_frame)
    info_frame.pack_forget()
    
    # creating lable that acts as headings
    headings=ttk.Label(info_frame,text='ID : Habit Name')
    headings.pack(padx=20,fill='x')

    # creating a listbox for habits display
    habits_listbox=tk.Listbox(info_frame,selectmode=tk.SINGLE,bd=2,relief=tk.SUNKEN)
    habits_listbox.pack(padx=20,pady=10,fill=tk.BOTH,side='left')

    # creating scrollbar for listbox
    scrollbar=ttk.Scrollbar(info_frame,orient=tk.VERTICAL,command=habits_listbox.yview)
    scrollbar.pack(side='left',fill='y')
    
    # linking scrollbar to listbox
    habits_listbox.config(yscrollcommand=scrollbar.set)

    ### creating action frame
    action_frame=ttk.Frame(display_frame)
    action_frame.pack_forget()

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

    # Row 2 frequency | edit frequency(menu)
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

    save_button=ttk.Button(action_frame,text='Save', command=save_edit)
    save_button.grid_forget()

    cancel_button=ttk.Button(action_frame,text='Cancel',command= cancel_edit)
    cancel_button.grid_forget()

    # Row 6 end button(for active) | start(for inactive)
    end_button=ttk.Button(action_frame,text='End',command=end_habit)
    end_button.grid_forget()

    start_button=ttk.Button(action_frame,text='Start',command=start_habit)
    start_button.grid_forget()

    # calling initial function
    show_user_habits()



