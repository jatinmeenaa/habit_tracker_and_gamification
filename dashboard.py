''' module for initializing user dashboard window '''

import tkinter as tk
from tkinter import ttk

import user
import db
from profile_tab import profile_tab

def dashboard(username):
    dash=tk.Toplevel()
    dash.grab_set()
    dash.title('Habit Tracker and Gamification')
    dash.geometry('600x400')

    #creating user instance
    user_instance=user.create_user(username)

    # default style
    style=ttk.Style()
    style.configure('TNotebook.Tab',padding=[20,5])
    style.configure('TFrame',background='light grey')
    
    #creating notebook for tabbed interface
    notebook=ttk.Notebook(dash)
    notebook.pack(expand=True,fill='both')

    # creating frames\tabs and adding them to notebook
    home=ttk.Frame(notebook)
    notebook.add(home,text='Home')
    habits=ttk.Frame(notebook)
    notebook.add(habits,text='Habits')
    habit_log=ttk.Frame(notebook)
    notebook.add(habit_log,text='Habit_Logs')
    rewards=ttk.Frame(notebook)
    notebook.add(rewards,text='Rewards')
    profile=ttk.Frame(notebook)
    notebook.add(profile,text='Profile')

    profile_tab(dash,profile,user_instance)
    
    dash.wait_window()
    return dash

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    dashboard("alice_smith")  # Open dashboard with a sample username
    root.destroy()
    root.mainloop()


