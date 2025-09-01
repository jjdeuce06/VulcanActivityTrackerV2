import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from database.db import get_user_info, insert_user
from .portal import UserPortal
import os
from PIL import Image, ImageTk

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Vulcan Activity Tracker")
        self.root.geometry("1000x600+200+100")
        self.root.configure(bg='#f0f2f5')
        self.root.resizable(False, False)
        self.img = None

        # Define modern colors
        self.PRIMARY_COLOR = '#2c3e50'
        self.SECONDARY_COLOR = '#3498db'
        self.ACCENT_COLOR = '#e74c3c'
        self.BG_COLOR = '#f0f2f5'
        self.TEXT_COLOR = '#2c3e50'
        
        self.build_login()

    def build_login(self):
            # print(os.path.exists('imgs/cu.png'))
            # img = Image.open("imgs/cu.png")
            # print(img.format, img.size, img.mode)
        # Create main container
            self.main_container = Frame(self.root, bg=self.BG_COLOR)
            self.main_container.pack(fill='both', expand=True, padx=20, pady=20)

            # Left side image container
            self.image_container = Frame(self.main_container, bg=self.BG_COLOR)
            self.image_container.pack(side='left', fill='both', expand=True, padx=(0, 20))
            
            # Title with better styling
            self.titlelabel = Label(self.image_container, text='Activity Tracker', 
                                fg=self.PRIMARY_COLOR, bg=self.BG_COLOR,
                                font=('Helvetica', 28, 'bold'))
            self.titlelabel.pack(pady=(0, 20))
            
            # Load Image with better styling
            self.img = PhotoImage(file='imgs/cu.png')
            Label(self.image_container, image=self.img, bg=self.BG_COLOR).pack(pady=50)


            # Right side login container
            self.login_frame = Frame(self.main_container, bg='white', 
                                highlightbackground=self.PRIMARY_COLOR,
                                highlightthickness=2)
            self.login_frame.pack(side='right', fill='both', expand=True, padx=(0, 0))
            self.login_frame.pack_propagate(False)

            # Heading with better styling
            self.heading = Label(self.login_frame, text='Sign In', 
                            fg=self.PRIMARY_COLOR, bg='white',
                            font=('Helvetica', 24, 'bold'))
            self.heading.pack(pady=(40, 30))

            # Username input with better styling
            self.user = Entry(self.login_frame, width=25, fg=self.TEXT_COLOR, 
                            border=0, bg='white',
                            font=('Helvetica', 12))
            self.user.pack(pady=(0, 10))
            self.user.insert(0, 'Username')
            self.user.bind('<FocusIn>', self.on_enter_user)
            self.user.bind('<FocusOut>', self.on_leave_user)
            Frame(self.login_frame, width=300, height=2, bg=self.PRIMARY_COLOR).pack(pady=(0, 20))

            # Password input with better styling
            self.code = Entry(self.login_frame, width=25, fg=self.TEXT_COLOR, 
                            border=0, bg='white',
                            font=('Helvetica', 12), show="*")
            self.code.pack(pady=(0, 10))
            self.code.insert(0, 'Password')
            self.code.bind('<FocusIn>', self.on_enter_code)
            self.code.bind('<FocusOut>', self.on_leave_code)
            Frame(self.login_frame, width=300, height=2, bg=self.PRIMARY_COLOR).pack(pady=(0, 20))

            # Sign In Button with better styling
            Button(self.login_frame, width=20, pady=8, text='Sign In', 
                  bg=self.SECONDARY_COLOR, fg='white', border=0,
                  font=('Helvetica', 11, 'bold'),
                  command=self.signin).pack(pady=(20, 30))

            # Sign Up section with better styling
            signup_frame = Frame(self.login_frame, bg='white')
            signup_frame.pack()
            
            Label(signup_frame, text="Don't have an account?", 
                 fg=self.TEXT_COLOR, bg='white',
                 font=('Helvetica', 10)).pack(side='left', padx=(0, 10))

            Button(signup_frame, text='Sign Up', 
                bg=self.SECONDARY_COLOR, fg='white',
                border=0, font=('Helvetica', 10, 'bold'),
                command=self.signup).pack(side='right')

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

    


