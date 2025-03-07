''' Main Window '''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as pop

import dashboard
import register
import user_authentication_registration


def show_password():
    '''function for showing entered password '''
    if pass_entry.cget('show')=='*':
        pass_entry.configure(show='')
    else :
        pass_entry.configure(show='*')

def sign_up(event):
    ''' function for registering new user 
    uses register_newuser from register module'''
    root.withdraw()
    username=register.register_newuser()
    if username:
        print(username)
        dashboard.dashboard(username)
        root.deiconify()
    else:
        root.deiconify()
        
def login_user():
    ''' funtion for user login'''
    username=user_entry.get().strip()
    password=pass_entry.get().strip()
    if username :
        if password :
            if user_authentication_registration.is_user_authentic(username,password):
                user_entry.delete(0,tk.END)
                pass_entry.delete(0,tk.END)
                root.withdraw()
                dash_window=dashboard.dashboard(username)
                root.deiconify()
            else:
                user_entry.delete(0,tk.END)
                pass_entry.delete(0,tk.END)
                pop.showerror('Invalid credentials','Entered username or password is invalid')
        else:
            pop.showinfo('Password','Enter password')
    else:
        pop.showinfo('Username',"Enter Username")


root=tk.Tk()
root.title('Habit Tracker and Gamification')
root.geometry('600x400')
root.config(bg='light grey')

#setting default style
style=ttk.Style()
style.configure('TLabel',background='light grey',forground='black',font=('Arial',10))
style.configure('TFrame',background='light grey')
style.configure("TCheckbutton", background="light grey")

#log in label
style.configure('login.TLabel',foreground='royal blue',font=('Arial',20,'bold'))
login=ttk.Label(root,text='Login',style='login.TLabel')
login.pack(pady=30)

#username frame
uframe=ttk.Frame(root)
uframe.pack(pady=10)
user_label=ttk.Label(uframe,text='Username :')
user_label.pack(side='left',padx=10)
user_entry=ttk.Entry(uframe,width=25)
user_entry.pack(side='left',padx=10)

#password frame
pframe=ttk.Frame(root)
pframe.pack(pady=10)
pass_label=ttk.Label(pframe,text='Password :')
pass_label.pack(side='left',padx=10)
pass_entry=ttk.Entry(pframe,show='*',width=25)
pass_entry.pack(side='left',padx=10)
show_var=tk.BooleanVar()
show=ttk.Checkbutton(root,text='show password',variable=show_var,command=show_password)
show.pack(pady=5)

# login button
login_button=ttk.Button(root,text='Login',command=login_user)
login_button.pack(pady=10)

# register user
rframe=ttk.Frame(root)
rframe.pack(pady=10)
label1=ttk.Label(rframe,text="don't have an account?")
label1.pack(side='left',padx=5)
label2=ttk.Label(rframe,text='sign up',foreground='blue',cursor='hand2',font=('Arial',9,'underline') )
label2.pack(side='left',padx=5)
label2.bind('<Button-1>',sign_up)


root.mainloop()