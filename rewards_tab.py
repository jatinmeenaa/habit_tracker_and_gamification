''' This module handles funtionality of rewards tab'''

import tkinter as tk
from tkinter import ttk

import db

def rewards_tab(dash,rewards,user_instance):

    # style
    style=ttk.Style()
    style.configure('TLabel',font=('Arial',10))
    style.configure('Label2.TLabel',foreground='dark green')

    ## total_points_frame
    total_points_frame=ttk.Frame(rewards)
    total_points_frame.pack(padx=20,pady=(30,5))

    # total_points_label1
    total_points_label1=ttk.Label(total_points_frame,text='Total Points : ')
    total_points_label1.pack(padx=10,side='left')
    
    total_points=db.get_user_total_points(user_instance.user_id)

    #total_points_label2
    total_points_label2=ttk.Label(total_points_frame,text=f'{total_points}',style='Label2.TLabel')
    total_points_label2.pack(padx=10,side='left')

    ## rank_frame
    rank_frame=ttk.Frame(rewards)
    rank_frame.pack(padx=20,pady=5)

    # rank_label1
    rank_label1=ttk.Label(rank_frame,text='Rank : ')
    rank_label1.pack(padx=10,side='left')

    rank=db.get_user_rank(user_instance.user_id)

    # rank_label2
    rank_label2=ttk.Label(rank_frame,text=f'{rank}',style='Label2.TLabel')
    rank_label2.pack(padx=10,side='left')

    ## consistency_frame
    consistency_frame=ttk.Frame(rewards)
    consistency_frame.pack(padx=20,pady=5)

    # consistency_label1
    consistency_label1=ttk.Label(consistency_frame,text='Consistency : ')
    consistency_label1.pack(padx=10,side='left')

    consistency=db.get_user_consistency(user_instance.user_id)

    # consistency_label2
    consistency_label2=ttk.Label(consistency_frame,text=f'{consistency} %',style='Label2.TLabel')
    consistency_label2.pack(padx=10,side='left')

    ## leaders_frame
    leaders_frame=ttk.Frame(rewards)
    leaders_frame.pack(padx=20,pady=5)

    # leaders_label
    leaders_label=ttk.Label(leaders_frame, text='Leaderboard')
    leaders_label.pack(padx=10,pady=5)

    # leaders_treeview
    columns=('User ID','Username','Total Points')
    leaders_treeview=ttk.Treeview(leaders_frame,columns=columns,show='headings')
    for column in columns:
        leaders_treeview.heading(column,text=column)
        leaders_treeview.column(column,width=100)
    
    leaders=db.get_leaders()

    for row in leaders:
        leaders_treeview.insert('',tk.END,values=row)

    leaders_treeview.pack()