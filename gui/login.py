import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from database.db import get_user_info, insert_user
from .portal import UserPortal

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.login = tk.Tk()
        self.login.title("Vulcan Activity Tracker")
        self.login.geometry("1000x600+200+100")
        self.login.configure(bg='#f0f2f5')
        self.login.resizable(False, False)
        self.img = None

        # Define modern colors
        self.PRIMARY_COLOR = '#2c3e50'
        self.SECONDARY_COLOR = '#3498db'
        self.ACCENT_COLOR = '#e74c3c'
        self.BG_COLOR = '#f0f2f5'
        self.TEXT_COLOR = '#2c3e50'
        
        self.build_login()

    def build_login(self):
        # Username input with better styling
            self.user = Entry(self.login, width=25, fg=self.TEXT_COLOR, 
                            border=0, bg='white',
                            font=('Helvetica', 12))
            self.user.pack(pady=(0, 10))
            self.user.insert(0, 'Username')
            self.user.bind('<FocusIn>', self.on_enter_user)
            self.user.bind('<FocusOut>', self.on_leave_user)

            self.code = Entry(self.login, width=25, fg=self.TEXT_COLOR, 
                            border=0, bg='white',
                            font=('Helvetica', 12), show="*")
            self.code.pack(pady=(0, 10))
            self.code.insert(0, 'Password')
            self.code.bind('<FocusIn>', self.on_enter_code)
            self.code.bind('<FocusOut>', self.on_leave_code)

            Button(self.root, text="Sign In", command=self.signin, bg=self.SECONDARY_COLOR, fg="white").pack(pady=10)
            Button(self.root, text="Sign Up", command=self.signup, bg=self.ACCENT_COLOR, fg="white").pack(pady=10)

    #---------USER-----------------#
    def on_enter_user(self, e):
            self.user.delete(0, 'end')

    def on_leave_user(self, e):
        name = self.user.get()
        if name == '':
            self.user.insert(0, 'Username')
    #---------END USER--------------#

    #---------PASSWORD---------------------#
    def on_enter_code(self, e):
        self.code.delete(0, 'end')

    def on_leave_code(self, e):
        name = self.code.get()
        if name == '':
            self.code.insert(0, 'Password')
    #---------END PASSWORD-------------------#

    def signin(self):
        username = self.user.get()
        password = self.code.get()
        row = get_user_info(username)
        if row and row[1] == password:
                self.open_portal(username)
        else:
            messagebox.showerror("Invalid", "Invalid credentials")
    
    def signup(self):
        signup_window = Toplevel(self.root)
        signup_window.title("Create Account")
        signup_window.geometry("400x300")

        Label(signup_window, text = "First name").pack()
        fname_entry = Entry(signup_window); fname_entry.pack()
        Label(signup_window, text = "Last name").pack()
        lname_entry = Entry(signup_window); lname_entry.pack()
        Label(signup_window, text="Age").pack()
        age_entry = Entry(signup_window); age_entry.pack()
        Label(signup_window, text = "Username").pack()
        username_entry = Entry(signup_window); username_entry.pack()
        Label(signup_window, text="Password").pack()
        password_entry = Entry(signup_window, show="*"); password_entry.pack()

        def confirm():
            insert_user(fname_entry.get(), lname_entry.get(), 
                        username_entry.get(), password_entry.get(),
                        int(age_entry.get()))
            signup_window.destroy()

        Button(signup_window, text="Confirm", command=confirm, bg=self.ACCENT_COLOR, fg="white").pack(pady=10)

    def open_portal(self, username):
        UserPortal(self.root, username)

    


