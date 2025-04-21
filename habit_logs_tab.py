''' This module handles funtionality of habit_logs tab'''

import tkinter as tk
from tkinter import ttk

import db

def habit_logs_tab(dash,habit_logs,user_instance):

    def show_not_done_habits():
        
        # set the guide label
        guide_label.config(text='Not Done')

        # update the layout
        global user_not_done_habits 
        user_not_done_habits=db.get_user_habits_with_status(user_instance.user_id,not_done=True)
        populate_listbox(user_not_done_habits)
        
        skipped_frame.pack_forget()
        done_frame.pack_forget()
        not_done_frame.pack(fill=tk.BOTH,expand=True)

    def show_skipped_habits():
        print('success')

    def show_done_habits():
        print('success')

    def populate_listbox(habits_entry):
        listbox.delete(0,tk.END)
        for user_habit_id,habit_name in habits_entry:
            listbox.insert(tk.END,f'{user_habit_id} : {habit_name}')

    def habits_done():
        print('success')

    def habits_skipped():
        print('success')

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
    menu.add_command(label='Not Done',command=show_not_done_habits)
    menu.add_separator()
    menu.add_command(label='Skipped',command=show_skipped_habits)
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
    done_button=ttk.Button(not_done_frame,text='Done',command= habits_done)
    done_button.grid(row=1,column=1,padx=20,pady=(20,10))

    # skip button
    skip_button=ttk.Button(not_done_frame,text='Skip',command=habits_skipped)
    skip_button.grid(row=2,column=1,padx=20,pady=10)

    ## skipped frame
    skipped_frame=ttk.Frame(content_frame)
    skipped_frame.pack_forget()

    ## done frame
    done_frame=ttk.Frame(content_frame)
    done_frame.pack_forget()