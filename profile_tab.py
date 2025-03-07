''' This module handles funtionality of profile tab'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

import db
import user_authentication_registration

def profile_tab(dash,profile,user_instance):

    def edit_info():
        
        # replace username value with entry
        username_val.grid_forget()
        username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
        # replace email value with entry
        email_val.grid_forget()
        email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # making other buttons invisible
        edit.grid_forget()
        change_p.grid_forget()
        log_out.grid_forget()
        delete.grid_forget()
        
        # making save and cancel button visible
        save_button.grid(row=6,column=0,padx=10,pady=5)
        cancel_button.grid(row=6,column=1,padx=10,pady=5)

    def revert_edit_layout():
        
        #revert widget changes
        username_entry.grid_forget()
        username_val.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        email_entry.grid_forget()
        email_val.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        save_button.grid_forget()
        cancel_button.grid_forget()

        edit.grid(row=6, column=0 ,padx=10 ,pady=5, sticky="w")
        change_p.grid(row=7, column=0 ,padx=10 ,pady=5, sticky="w")
        log_out.grid(row=8, column=0 ,padx=10 ,pady=5, sticky="w")
        delete.grid(row=9, column=0 ,padx=10 ,pady=5, sticky="w")

    def  save_info():
        username_update_flag=0
        email_update_flag=0
        username=username_entry.get().strip()
        email=email_entry.get().strip()
        if username==user_instance.username :
            pass # flag remain zero
        else:
            if user_authentication_registration.is_username_valid(username):
                if user_authentication_registration.username_exists(username):
                    messagebox.showerror('Username Taken','This username is already in use. Please choose a different one')
                    return
                else:
                    username_update_flag=1
            else:
                messagebox.showerror('Invalid Username','The username you entered is not valid. Please try again.')
                return         

        if email==user_instance.email :
            pass # flag remain zero
        else:
            if user_authentication_registration.is_email_valid(email):
                if user_authentication_registration.email_exists(email):
                    messagebox.showerror('Email Taken','This email is already in use. Please choose a different one')
                    return
                else:
                    email_update_flag=1
            else:
                messagebox.showerror('Invalid Email','The email you entered is not valid. Please try again.')
                return
        if username_update_flag:
            user_authentication_registration.update_username(username,user_instance.user_id)
        if email_update_flag:
            user_authentication_registration.update_email(email,user_instance.user_id)

        messagebox.showinfo('Changes saved','Your details have been successfully updated.')

        user_instance.username=username
        user_instance.email=email
        username_val.config(text=user_instance.username)
        email_val.config(text=user_instance.email)
        revert_edit_layout()

    def log_out_user():
        if messagebox.askyesno('Confirm Logout','"Are you sure you want to log out?"'):
            dash.destroy()

    def delete_account():
        password=simpledialog.askstring('Password','Enter Password').strip()
        if password and user_authentication_registration.is_user_authentic(user_instance.username,password):
            if messagebox.askyesno('Confirm Account Deletion','Are you sure you want to delete your account? This action cannot be undone.'):
                db.delete_user(user_instance.user_id)
                dash.destroy()
                messagebox.showinfo('Successful Deletion','The user has been deleted successfully')
        else:
            messagebox.showerror('Incorrect Password','The password you entered is incorrect. Please try again.')

    def change_password():
        password=simpledialog.askstring('Password','Enter Password')
        if password :
            password=password.strip()
        else: 
            return 
        if password and user_authentication_registration.is_user_authentic(user_instance.username,password):
            new_password=simpledialog.askstring('New Password','Enter New Password',parent=dash)
            if new_password:
                new_password=new_password.strip()
                if user_authentication_registration.is_valid_and_strong(new_password):
                    user_authentication_registration.change_user_password(new_password,user_instance.user_id)
                    messagebox.showinfo('Password Changed','Your password has been successfully changed.')
                else:
                    messagebox.showerror('Password Error','''1. Must be at least 8 characters long.
    2. Must contain at least one lowercase letter (a-z).
    3. Must contain at least one uppercase letter (A-Z).
    4. Must contain at least one digit (0-9).
    5. Must contain at least one special character (@#$%^&+=!).
    6. No spaces allowed.''')
            else:
                pass
        else:
            messagebox.showerror('Incorrect Password','The password you entered is incorrect. Please try again.')

    
    # style for the information labels
    style = ttk.Style()
    style.configure("Label.TLabel", font=("Arial", 10), foreground="black",background='light grey')
    style.configure("Info.TLabel", font=("Arial", 10), foreground="dark green",background='light grey')

    # Row 0: User ID
    user_id_label = ttk.Label(profile, text="User ID:", style="Label.TLabel")
    user_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    user_id_val = ttk.Label(profile, text=user_instance.user_id, style="Info.TLabel")
    user_id_val.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Row 1: Username
    username_label = ttk.Label(profile, text="Username:", style="Label.TLabel")
    username_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    username_val = ttk.Label(profile, text=user_instance.username, style="Info.TLabel")
    username_val.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Username entry
    username_entry = ttk.Entry(profile, text=user_instance.username,width=30)
    username_entry.insert(0,user_instance.username)
    username_entry.grid_forget()

    # Row 2: Email
    email_label = ttk.Label(profile, text="Email:", style="Label.TLabel")
    email_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    email_val = ttk.Label(profile, text=user_instance.email, style="Info.TLabel")
    email_val.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Email entry
    email_entry = ttk.Entry(profile, text=user_instance.email,width=30)
    email_entry.insert(0,user_instance.email)
    email_entry.grid_forget()

    # Row 3: Total Points
    points_label = ttk.Label(profile, text="Total Points:", style="Label.TLabel")
    points_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    points_val = ttk.Label(profile, text=user_instance.total_points, style="Info.TLabel")
    points_val.grid(row=3, column=1, padx=10, pady=5, sticky="w")    

    # Edit button
    edit=ttk.Button(profile,text='Edit Info',command=edit_info)
    edit.grid(row=6,column=0,padx=10,pady=5)

    # Save button
    save_button=ttk.Button(profile,text='Save',command=save_info)
    save_button.grid_forget()

    # Cancel button
    cancel_button=ttk.Button(profile,text='Cancel',command=revert_edit_layout)
    cancel_button.grid_forget()

    # Change password button
    change_p=ttk.Button(profile,text='Change Password',command=change_password)
    change_p.grid(row=7,column=0,padx=10,pady=5)

    # Log out button
    log_out=ttk.Button(profile,text='Log Out',command=log_out_user)
    log_out.grid(row=8,column=0,padx=10,pady=5)

    # Delete account
    delete=ttk.Button(profile,text='Delete Account',command=delete_account)
    delete.grid(row=9,column=0,padx=10,pady=5)

        