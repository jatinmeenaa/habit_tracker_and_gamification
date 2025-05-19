''' This module handles funtionality of habit_logs tab'''

import tkinter as tk
from tkinter import ttk

import db

def habit_logs_tab(dash,habit_logs,user_instance):

    def show_not_done_habits():
        ''' Function to add habits to listbox and change layout when not done option choosen'''

        # set the guide label
        guide_label.config(text='Not Done')

        # update the layout
        user_not_done_habits=db.get_user_habits_with_status(user_instance.user_id,not_done=True)
        populate_listbox(user_not_done_habits)
        
        skipped_frame.pack_forget()
        done_frame.pack_forget()
        not_done_frame.pack(fill=tk.BOTH,expand=True)

    def show_skipped_habits():
        ''' Function to add habits to listbox and change layout when skipped option choosen'''

        # set the guide label
        guide_label.config(text='Skipped')

        # update the layout
        user_skipped_habits=db.get_user_habits_with_status(user_instance.user_id,skipped=True)
        populate_listbox(user_skipped_habits)
        
        not_done_frame.pack_forget()
        done_frame.pack_forget()
        skipped_frame.pack(fill=tk.BOTH,expand=True)

    def show_done_habits():
        ''' Function to add habits to listbox and change layout when done option choosen'''

        # set the guide label
        guide_label.config(text='Done')

        # update the layout
        user_done_habits=db.get_user_habits_with_status(user_instance.user_id,done=True)
        populate_listbox(user_done_habits)
        
        not_done_frame.pack_forget()
        skipped_frame.pack_forget()
        done_frame.pack(fill=tk.BOTH,expand=True)

    def populate_listbox(habits_entry):
        '''Function to populate habits passed to it in form of list'''

        listbox.delete(0,tk.END)
        for user_habit_id,habit_name in habits_entry:
            listbox.insert(tk.END,f'{user_habit_id} : {habit_name}')

    def update_habit_log_status(from_current_list , to_current_list, not_done=False,skipped=False,done=False):
        '''Function to change the status of user_logs'''

        indexes=listbox.curselection()
        if(len(indexes)==0):
            return
        
        user_habit_id_list=[]
        for index in indexes:
            user_habit_id_list.append(from_current_list[index][0])
        
        db.update_habit_status(user_habit_id_list,skipped=skipped,not_done=not_done,done=done)
        #need to delete in right to left else index error
        for index in reversed(indexes):
            listbox.delete(index)
            to_current_list.append(from_current_list.pop(index))

    # global variable declaration
    global user_not_done_habits 
    user_not_done_habits=db.get_user_habits_with_status(user_instance.user_id,not_done=True)
    global user_skipped_habits 
    user_skipped_habits=db.get_user_habits_with_status(user_instance.user_id,skipped=True)
    global user_done_habits 
    user_done_habits=db.get_user_habits_with_status(user_instance.user_id,done=True)

    # styling 
    style=ttk.Style()

    ## menue and guide label frame
    menu_frame=ttk.Frame(habit_logs)
    menu_frame.pack(fill='x')

    # guide label
    guide_label=ttk.Label(menu_frame,text='')
    guide_label.pack(side='left',padx=20,pady=10)

    # menubutton
    menubutton=ttk.Menubutton(menu_frame,text='Habit Status')
    menubutton.pack(side='right',padx=20,pady=10)

    # habit status menu  
    menu=tk.Menu(menubutton,tearoff=0)
    menu.add_command(label='Skipped',command=show_skipped_habits)
    menu.add_separator()
    menu.add_command(label='Not Done',command=show_not_done_habits)
    menu.add_separator()
    menu.add_command(label='Done',command=show_done_habits)

    # configuring menubutton
    menubutton.config(menu=menu)

    ### main frame
    main_frame=ttk.Frame(habit_logs)
    main_frame.pack(fill=tk.BOTH,expand=True)

    ## listbox frame
    listbox_frame=ttk.Frame(main_frame)
    listbox_frame.pack(side='left',fill=tk.BOTH)
    
    # head label
    head_label=ttk.Label(listbox_frame,text='ID : Habit Name')
    head_label.pack(padx=20,fill='x')

    # listbox
    listbox=tk.Listbox(listbox_frame,selectmode=tk.MULTIPLE,bd=2,relief=tk.SUNKEN)
    listbox.pack(padx=20,pady=10,fill='both',side='left')

    # adding scrollbar
    scrollbar=ttk.Scrollbar(listbox_frame,orient=tk.VERTICAL,command=listbox.yview)
    scrollbar.pack(side='left',fill='y')

    listbox.config(yscrollcommand=scrollbar.set)

    ## content frame
    content_frame=ttk.Frame(main_frame)
    content_frame.pack(side='left',expand=True,fill=tk.BOTH)

    ## not_done frame
    not_done_frame=ttk.Frame(content_frame)
    not_done_frame.pack_forget()

    # done button
    done_button_nd=ttk.Button(not_done_frame,text='Done',command= lambda : update_habit_log_status(user_not_done_habits,user_done_habits,done=True))
    done_button_nd.grid(row=1,column=1,padx=20,pady=(20,10))

    # skip button
    skip_button_nd=ttk.Button(not_done_frame,text='Skip',command= lambda : update_habit_log_status(user_not_done_habits,user_skipped_habits,skipped=True))
    skip_button_nd.grid(row=2,column=1,padx=20,pady=10)

    ## skipped frame
    skipped_frame=ttk.Frame(content_frame)
    skipped_frame.pack_forget()

    # done button
    done_button_s=ttk.Button(skipped_frame,text='Done',command= lambda : update_habit_log_status(user_skipped_habits,user_done_habits,done=True))
    done_button_s.grid(row=1,column=1,padx=20,pady=(20,10))

    # not done button
    not_done_button_s=ttk.Button(skipped_frame,text='Not Done',command= lambda : update_habit_log_status(user_skipped_habits,user_not_done_habits,not_done=True))
    not_done_button_s.grid(row=2,column=1,padx=20,pady=10)

    ## done frame
    done_frame=ttk.Frame(content_frame)
    done_frame.pack_forget()

    # skip button
    skip_button_d=ttk.Button(done_frame,text='Skip',command= lambda : update_habit_log_status(user_done_habits,user_skipped_habits,skipped=True))
    skip_button_d.grid(row=1,column=1,padx=20,pady=(20,10))

    # not done button
    not_done_button_s=ttk.Button(done_frame,text='Not Done',command= lambda : update_habit_log_status(user_done_habits,user_not_done_habits,not_done=True))
    not_done_button_s.grid(row=2,column=1,padx=20,pady=10)

    show_skipped_habits()