import tkinter as tk
from tkinter import *
from database.db import (
    get_user_info, update_user_profile,
    insert_activity, get_activity_by_name
)
from models.Activity import Activity

class UserPortal:
    def __init__(self, root, username):
        self.username = username
        self.root = tk.Toplevel(root)
        self.root.title("Vulcan Activity Tracker")
        self.root.geometry("925x500+300+200")
        self.root.configure(bg="#f0f2f5")

        self.PRIMARY_COLOR = '#2c3e50'
        self.SECONDARY_COLOR = '#3498db'

        self.menu_frame = Frame(self.root, bg=self.PRIMARY_COLOR)
        self.menu_frame.pack(side=tk.LEFT, fill='y')

        Button(self.menu_frame, text="Home", command=self.total_page, bg=self.PRIMARY_COLOR, fg = "white").pack(pady=20)

        self.interactive_frame = Frame(self.root, bg="white")
        self.interactive_frame.pack(side=tk.LEFT, fill="both", expand=True)

        self.total_page()
    def clear_frame(self):
        for w in self.interactive_frame.winfo_children():
            w.destroy()
    
    def total_page(self):
        self.clear_frame()
        Label(self.interactive_frame, text=f"Welcome, {self.username}", font=("Helvetica", 18)).pack(pady=20)
        row = get_user_info(self.username)
        if row:
            Label(self.interactive_frame, text=f"Total Miles: {row[3]}").pack()
            Label(self.interactive_frame, text=f"Activities: {row[4]}").pack()

    def addActivity_page(self):
        self.clear_frame()
        Label(self.interactive_frame, text="Add Activity", font=("Helvetica", 18)).pack(pady=20)

        # entries...
        name_entry = Entry(self.interactive_frame); name_entry.pack()
        miles_entry = Entry(self.interactive_frame); miles_entry.pack()
        cals_entry = Entry(self.interactive_frame); cals_entry.pack()
        elev_entry = Entry(self.interactive_frame); elev_entry.pack()
        hr_entry = Entry(self.interactive_frame); hr_entry.pack()
        pace_entry = Entry(self.interactive_frame); pace_entry.pack()
        date_entry = Entry(self.interactive_frame); date_entry.pack()

        def submit():
            name = name_entry.get()
            miles = float(miles_entry.get())
            cals = int(cals_entry.get())
            elev = int(elev_entry.get())
            hr = int(hr_entry.get())
            pace = int(pace_entry.get())
            date = date_entry.get()
            zone = 20

            # Save to activities table
            insert_activity(self.username, name, miles, cals, elev, hr, pace, zone, date)

            # Update userProfile totals
            row = get_user_info(self.username)
            if row:
                new_miles = float(row[3]) + miles
                new_activities = int(row[4]) + 1
                update_user_profile(self.username, new_miles, new_activities)

            self.total_page()

        Button(self.interactive_frame, text="Submit", command=submit,
               bg=self.SECONDARY_COLOR, fg="white").pack(pady=10)

    def viewActivity_page(self):
        self.clear_frame()
        Label(self.interactive_frame, text="View Activity", font=("Helvetica", 18)).pack(pady=20)

        Label(self.interactive_frame, text="Enter Activity Name").pack()
        self.name_enter = Entry(self.interactive_frame)
        self.name_enter.pack(pady=10)

        Button(self.interactive_frame, text="Find Activity",
               command=self.getactivity,
               bg=self.SECONDARY_COLOR, fg="white").pack(pady=10)

        self.result_labels = {
            "name": Label(self.interactive_frame, text=""),
            "calories": Label(self.interactive_frame, text=""),
            "elevation": Label(self.interactive_frame, text=""),
            "zone": Label(self.interactive_frame, text=""),
            "pace": Label(self.interactive_frame, text=""),
            "hr": Label(self.interactive_frame, text=""),
            "date": Label(self.interactive_frame, text=""),
        }
        for lbl in self.result_labels.values():
            lbl.pack()

    def getactivity(self):
        name = self.name_enter.get()
        row = get_activity_by_name(self.username, name)
        if row:
            self.result_labels["name"].config(text=f"Name: {row['name']}")
            self.result_labels["calories"].config(text=f"Calories: {row['calories']}")
            self.result_labels["elevation"].config(text=f"Elevation: {row['elevation']}")
            self.result_labels["zone"].config(text=f"Zone: {row['zone']}")
            self.result_labels["pace"].config(text=f"Pace: {row['pace']}")
            self.result_labels["hr"].config(text=f"Heart Rate: {row['hr']}")
            self.result_labels["date"].config(text=f"Date: {row['date']}")
        else:
            self.result_labels["name"].config(text="No activity found")
            for key in self.result_labels:
                if key != "name":
                    self.result_labels[key].config(text="")
