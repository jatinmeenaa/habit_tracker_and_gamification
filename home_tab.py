''' This module handles funtionality of home tab'''

import tkinter as tk
from tkinter import ttk
import random

def home_tab(dash,home,user_instance):

    def configure_scroll(event):
        '''funtion to adjust scrollregion dynamically'''
        canvas.configure(scrollregion=canvas.bbox('all'))

    # styling
    style=ttk.Style()
    style.configure('TLabel',background='light grey')

    ## creating welcome frame
    welcome_frame=ttk.Frame(home)
    welcome_frame.pack(fill='x',side='top')
    # creating welcome label
    welcome=ttk.Label(welcome_frame,text=f'Welcome {user_instance.username} !!',background='light grey',foreground='blue',font=('Arial',12,'bold'))
    welcome.pack(padx=10,pady=10,side=tk.LEFT)

    ## quotes list
    quotes_list = [
    "Success isn't always about greatness. It's about consistency. Consistent hard work leads to success. — Dwayne Johnson",
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit. — Aristotle",
    "Small daily improvements are the key to staggering long-term results. — Robin Sharma",
    "Motivation gets you going, but discipline keeps you growing. — John C. Maxwell",
    "The secret of your future is hidden in your daily routine. — Mike Murdock",
    "Consistency is more important than perfection. — Unknown",
    "It’s not what we do once in a while that shapes our lives. It’s what we do consistently. — Tony Robbins",
    "Dream big, start small, but most of all, start. — Simon Sinek",
    "Success is the sum of small efforts, repeated day in and day out. — Robert Collier",
    "Don’t stop until you’re proud. — Unknown"
]

    ## creating quote frame
    quote_frame=ttk.Frame(home)
    quote_frame.pack(fill='x',side='top')
    # creating quote message
    quote_message=tk.Message(quote_frame,text=f'" {random.choice(quotes_list)} "',width=550,font=('Helvetica',11),fg='green',bg='light grey')
    quote_message.pack()

    ## creating features message
    features_dict = {
    "👤 Profile Management": [
        "View, edit, and delete your details.",
        "Logout securely anytime."
    ],
    "📅 Habit Management": [
        "Add, edit, or remove your habits.",
        "Set daily goals for consistency."
    ],
    "📈 Habit Logs": [
        "Track daily progress and view history.",
        "Analyze performance over time."
    ],
    "🎯 Rewards System": [
        "Earn points and badges for milestones.",
        "Stay motivated with gamified elements."
    ],
    "💬 Motivational Quotes": [
        "Daily inspiration to keep you going."
    ],
    "⚡ Quick Stats": [
        "View daily completion rate and streaks."
    ]
}

    ## creating canvas_main_frame
    canvas_main_frame=ttk.Frame(home)
    canvas_main_frame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

    # creating canvas
    canvas=tk.Canvas(canvas_main_frame,bg='light grey',highlightthickness=0)
    canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
    # creating scrollbar
    scrollbar=ttk.Scrollbar(canvas_main_frame,orient=tk.VERTICAL,comman=canvas.yview)
    scrollbar.pack(side=tk.RIGHT,fill='y')
    # creating scrollable frame
    sc_frame=ttk.Frame(canvas)
    # creating window for sc_frame
    canvas.create_window((0,0),window=sc_frame,anchor='nw')
    # binding configure event to adjust scrolling
    sc_frame.bind('<Configure>',configure_scroll)
    ## adding content to sc_frame
    
    ## creating description message
    description='"Habit Tracker with Gamification"'+" is designed to help you build and maintain positive habits through consistency and motivation. By tracking daily habits, logging progress, and rewarding achievements, this tool makes self-improvement engaging and fun. Whether you're building a new habit or breaking an old one, staying consistent has never been easier!"
    description_message=tk.Message(sc_frame,text=description,width=500,font=('Arial',10),background='light grey')
    description_message.pack(pady=(30,5))
    for feature,details in features_dict.items():
        ttk.Label(sc_frame,text=feature,font=('Arial',12),foreground='blue').pack(pady=(15,4),anchor='w')
        for detail in details:
            ttk.Label(sc_frame,text=f'- {detail}',font=('Arial',10)).pack(anchor='w')
    # configure canvas to sync to scrollbar
    canvas.config(yscrollcommand=scrollbar.set)