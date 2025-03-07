''' Module for registering new user '''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import bcrypt

import user_authentication_registration
import db

def register_newuser():
    '''function for user registration window'''

    username_var=tk.StringVar()

    def check_email(email):
        '''function for checking if the entered email is valid and not already registered'''
        
        if user_authentication_registration.is_email_valid(email):
            pass
        else:
            messagebox.showerror('Invalid Email','Please enter a valid email')
            return 

        if user_authentication_registration.email_exists(email):
            messagebox.showerror('Registration Error',"This email is already registered. Please use a different email or log in.")
            email_entry.delete(0,tk.END)
        else:
            eframe.pack_forget()
            submit_button.pack_forget()
            user_pass_frame.pack(pady=10)

    def show_password():
        '''function for showing entered password '''
        if p_pass_entry.cget('show')=='*':
            p_pass_entry.configure(show='')
            c_pass_entry.configure(show='')
        else :
            p_pass_entry.configure(show='*')
            c_pass_entry.configure(show='*')

    def is_username_taken(event):
        '''Function to check if the username is taken'''

        username=user_entry.get().strip()
        if username in username_list:
            username_exist_label.config(text='username is taken')
            info_submit.config(state=tk.DISABLED)
        else:
            username_exist_label.config(text='')
            info_submit.config(state=tk.NORMAL)

    def check_entries():
        ''' Funtion to check if the entries username,password is valid'''

        username=user_entry.get().strip()

        if user_authentication_registration.is_username_valid(username):
            create_p=p_pass_entry.get().strip()
            confirm_p=c_pass_entry.get().strip()
            if create_p==confirm_p:
                if user_authentication_registration.is_valid_and_strong(create_p):
                    user_authentication_registration.register_user(email_entry.get().strip(),username,create_p)
                    messagebox.showinfo('Registration Successful','user has been registered successfully.')
                    username_var.set(username)
                    register.destroy()
                    
                else:
                    messagebox.showerror('Password Error','''1. Must be at least 8 characters long.
2. Must contain at least one lowercase letter (a-z).
3. Must contain at least one uppercase letter (A-Z).
4. Must contain at least one digit (0-9).
5. Must contain at least one special character (@#$%^&+=!).
6. No spaces allowed.''')
            else:
                messagebox.showerror('Password Missmatch','Confirm password does not match to New password')
        else:
            messagebox.showerror('Invalid Username','Username can contain letters (A-Z, a-z), numbers (0-9) and underscores (_) only ')

    username_list=db.get_usernames()

    #creating and configuring registration window
    register=tk.Toplevel()
    register.grab_set()
    register.title('Habit Tracker and Gamification')
    register.geometry('600x400')
    register.config(bg='light grey')

    #setting default style
    style=ttk.Style()
    style.configure('TLabel',background='light grey',forground='black',font=('Arial',10))
    style.configure('TFrame',background='light grey')
    style.configure("TCheckbutton", background="light grey")

    #log in label
    style.configure('Sign_up.TLabel',foreground='royal blue',font=('Arial',20,'bold'))
    Sign_up=ttk.Label(register,text='Sign Up',style='Sign_up.TLabel')
    Sign_up.pack(pady=30)

    # email frame
    eframe=ttk.Frame(register)
    eframe.pack(pady=10)
    email_label=ttk.Label(eframe,text='Enter your email :')
    email_label.pack(side='left',pady=10)
    email_entry=ttk.Entry(eframe,width=25)
    email_entry.pack(side='left',pady=10)

    # submit button
    submit_button=ttk.Button(register,text='Submit',command=lambda:check_email(email_entry.get().strip()))
    submit_button.pack(pady=10)

    # user pass frame
    user_pass_frame=ttk.Frame(register)
    user_pass_frame.pack_forget()

    #username frame
    uframe=ttk.Frame(user_pass_frame)
    uframe.pack(pady=10)
    user_label=ttk.Label(uframe,text='Username :')
    user_label.pack(side='left',padx=10)
    user_entry=ttk.Entry(uframe,width=25)
    user_entry.pack(side='left',padx=10)
    user_entry.bind('<KeyRelease>',is_username_taken)

    # label if user name is taken
    username_exist_label=ttk.Label(user_pass_frame,text='',foreground='red',font=('Arial',8))
    username_exist_label.pack()

    # password frame
    p_frame=ttk.Frame(user_pass_frame)
    p_frame.pack(pady=10)
    p_pass_label=ttk.Label(p_frame,text='New Password :')
    p_pass_label.pack(side='left',padx=10)
    p_pass_entry=ttk.Entry(p_frame,show='*',width=25)
    p_pass_entry.pack(side='left',padx=10)

    # confirm password frame
    c_frame=ttk.Frame(user_pass_frame)
    c_frame.pack(pady=10)
    c_pass_label=ttk.Label(c_frame,text='Confirm Password :')
    c_pass_label.pack(side='left',padx=10)
    c_pass_entry=ttk.Entry(c_frame,show='*',width=25)
    c_pass_entry.pack(side='left',padx=10)

    #show password checkbox
    show_var=tk.BooleanVar()
    show=ttk.Checkbutton(user_pass_frame,text='show password',variable=show_var,command=show_password)
    show.pack(pady=5)

    # submit button 
    info_submit=ttk.Button(user_pass_frame,text='Submit',command=check_entries)
    info_submit.pack(pady=20)

    register.wait_window()
    return username_var.get()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    register_newuser()  # Open registration window
    root.destroy()
    root.mainloop()
