import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from tkinter import simpledialog
from tkcalendar import Calendar, DateEntry
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

        # Define modern colors
        self.PRIMARY_COLOR = '#2c3e50'
        self.SECONDARY_COLOR = '#3498db'
        self.ACCENT_COLOR = '#e74c3c'
        self.BG_COLOR = '#f0f2f5'
        self.TEXT_COLOR = '#2c3e50'

        self.menu_frame = Frame(self.root, bg=self.PRIMARY_COLOR)
        self.menu_frame.pack(side=tk.LEFT, fill='y')

        Button(self.menu_frame, text="Home", command=self.total_page, bg=self.PRIMARY_COLOR, fg = "white").pack(pady=20)
        Button(self.menu_frame, text="Add Activity", command=self.addActivity_page, bg=self.PRIMARY_COLOR, fg = "white").pack(pady=20)
        Button(self.menu_frame, text="View Activity", command=self.viewActivity_page, bg=self.PRIMARY_COLOR, fg = "white").pack(pady=20)

        self.interactive_frame = Frame(self.root, bg="white")
        self.interactive_frame.pack(side=tk.LEFT, fill="both", expand=True)

        self.total_page()
    def clear_frame(self):
        for w in self.interactive_frame.winfo_children():
            w.destroy()
    
    def total_page(self):
        self.clear_frame()
        Label(self.interactive_frame, text=f"Welcome, {self.username}", font=("Helvetica", 35)).pack(pady=20)
        row = get_user_info(self.username)
        if row:
            Label(self.interactive_frame, text=f"Total Miles: {row[3]}").pack()
            Label(self.interactive_frame, text=f"Activities: {row[4]}").pack()

    def addActivity_page(self):
        self.clear_frame()
        Label(self.interactive_frame, text="Add Activity", font=("Helvetica", 18)).pack(pady=20)

        # Modern heading
        heading = Label(self.interactive_frame,
                        text='Add Activity',
                        fg=self.PRIMARY_COLOR,
                        bg=self.BG_COLOR,
                        font=('Helvetica', 28, 'bold'))
        heading.pack(pady=20)

        # Main container with two columns
        main_container = Frame(self.interactive_frame, bg=self.BG_COLOR)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Left side for inputs
        input_frame = Frame(main_container,
                            bg='white',
                            highlightbackground=self.PRIMARY_COLOR,
                            highlightthickness=1)
        input_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Right side for calendar
        calendar_frame = Frame(main_container,
                                bg='white',
                                highlightbackground=self.PRIMARY_COLOR,
                                highlightthickness=1)
        calendar_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # Calendar widget for activity date
        Label(calendar_frame, text="Select Date", fg=self.PRIMARY_COLOR, bg='white', font=('Helvetica', 12, 'bold')).pack(pady=(20, 5))
        self.activity_date = Calendar(calendar_frame, selectmode="day", date_pattern='yyyy-mm-dd')
        self.activity_date.pack(pady=10)

        # Modern input styles
        entry_style = {'width': 25,
                        'fg': self.TEXT_COLOR,
                        'bg': 'white',
                        'font': ('Helvetica', 12),
                        'bd': 2,
                        'relief': 'solid'}

        label_style = {'fg': self.PRIMARY_COLOR,
                        'bg': 'white',
                        'font': ('Helvetica', 12, 'bold')}

        # Input fields container
        fields_container = Frame(input_frame, bg='white')
        fields_container.pack(padx=30, pady=20, fill='both', expand=True)

        # Miles input
        Label(fields_container, text="Miles Ran", **label_style).pack(anchor='w', pady=(0, 5))
        self.add_miles = Entry(fields_container, **entry_style)
        self.add_miles.insert(0, 'Enter miles')
        self.add_miles.bind('<FocusIn>', self.on_enter_miles)
        self.add_miles.bind('<FocusOut>', self.on_exit_miles)
        self.add_miles.pack(anchor='w', pady=(0, 15))

        # Calories input
        Label(fields_container, text="Calories Burned", **label_style).pack(anchor='w', pady=(0, 5))
        self.add_cals = Entry(fields_container, **entry_style)
        self.add_cals.insert(0, 'Enter calories')
        self.add_cals.bind('<FocusIn>', self.on_enter_cals)
        self.add_cals.bind('<FocusOut>', self.on_exit_cals)
        self.add_cals.pack(anchor='w', pady=(0, 15))

        # Elevation input
        Label(fields_container, text="Elevation Gained", **label_style).pack(anchor='w', pady=(0, 5))
        self.elev_enter = Entry(fields_container, **entry_style)
        self.elev_enter.insert(0, 'Enter elevation')
        self.elev_enter.bind('<FocusIn>', self.on_enter_elev)
        self.elev_enter.bind('<FocusOut>', self.on_exit_elev)
        self.elev_enter.pack(anchor='w', pady=(0, 15))

        # Heart Rate input
        Label(fields_container, text="Average Heart Rate", **label_style).pack(anchor='w', pady=(0, 5))
        self.hr_entry = Entry(fields_container, **entry_style)
        self.hr_entry.insert(0, 'Enter heart rate')
        self.hr_entry.bind('<FocusIn>', self.hr_on_entry)
        self.hr_entry.bind('<FocusOut>', self.hr_on_exit)
        self.hr_entry.pack(anchor='w', pady=(0, 15))

        # Pace input
        Label(fields_container, text="Average Pace", **label_style).pack(anchor='w', pady=(0, 5))
        self.pace_entry = Entry(fields_container, **entry_style)
        self.pace_entry.insert(0, 'Enter pace')
        self.pace_entry.bind('<FocusIn>', self.pace_enter)
        self.pace_entry.bind('<FocusOut>', self.pace_exit)
        self.pace_entry.pack(anchor='w', pady=(0, 15))

        # Activity Name input
        Label(fields_container, text="Activity Name", **label_style).pack(anchor='w', pady=(0, 5))
        self.name_entry = Entry(fields_container, **entry_style)
        self.name_entry.insert(0, 'Enter activity name')
        self.name_entry.bind('<FocusIn>', self.name_enter)
        self.name_entry.bind('<FocusOut>', self.name_exit)
        self.name_entry.pack(anchor='w', pady=(0, 15))

        # Race checkbox
        self.raceCheck = Checkbutton(fields_container,
                                    text="Race Day",
                                    fg=self.PRIMARY_COLOR,
                                    bg='white',
                                    font=('Helvetica', 12))
        self.raceCheck.pack(anchor='w', pady=15)

        # Submit button
        self.update_button = Button(calendar_frame,
                text='Submit',
                bg=self.SECONDARY_COLOR,
                fg='white',
                border=0,
                font=('Helvetica', 12, 'bold'),
                command=self.updatedata)
        self.update_button.place(x=100, y=350, width=150, height=40)

        # Add hover effect
        self.update_button.bind('<Enter>', lambda e: self.update_button.config(bg=self.ACCENT_COLOR))
        self.update_button.bind('<Leave>', lambda e: self.update_button.config(bg=self.SECONDARY_COLOR))

        #self.total_page()

        # Button(self.interactive_frame, text="Submit", command=self.updatedata,
        #     bg=self.SECONDARY_COLOR, fg="white").pack(pady=10)

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


    def on_enter_miles(self, e):
        self.add_miles.delete(0, 'end')
    def on_exit_miles(self, e):
            if self.add_miles.get() == "":
                self.add_miles.delete(0, 'end')  # Clear the entry field
                self.add_miles.insert(0, 'Add miles here')
    def on_enter_cals(self, e):
            self.add_cals.delete(0, 'end')
    def on_exit_cals(self, e):
        if self.add_cals.get() == "":
                self.add_cals.delete(0, 'end')  # Clear the entry field
                self.add_cals.insert(0, 'Add calories here')
    def on_enter_elev(self, e):
            self.elev_enter.delete(0, 'end')
    def on_exit_elev(self, e):
            if self.elev_enter.get() == "":
                self.elev_enter.delete(0, 'end')
                self.elev_enter.insert(0, 'Add elevation here')
    def hr_on_entry(self, e):
            self.hr_entry.delete(0, 'end')
    def hr_on_exit(self, e):
            if self.hr_entry.get() == "":
                self.hr_entry.delete(0, 'end')
                self.hr_entry.insert(0, "Add heart rate here")
    def pace_enter(self, e):
            self.pace_entry.delete(0, 'end')
    def pace_exit(self, e):
            if self.pace_entry.get() == "":
                self.pace_entry.delete(0, 'end')
                self.pace_entry.insert(0, 'Add mile pace')
    def name_enter(self, e):
            self.name_entry.delete(0, 'end')
    def name_exit(self, e):
            if self.name_entry.get() == "":
                self.name_entry.delete(0, 'end')
                self.name_entry.insert(0, 'Add activity name')
    def updatedata(self):
                self.newmiles = self.add_miles.get()
                self.newcals = self.add_cals.get()
                self.new_elev = self.elev_enter.get()
                self.activites = int(self.activites) + 1
                self.new_name = self.name_entry.get()
                self.new_pace = self.pace_entry.get()
                self.new_hr = self.hr_entry.get()
                self.new_date = self.activity_date.get_date()
                #self.check_race = self.raceCheck.getboolean()

                #Add activity to the array
                data_added = False
                while(data_added == False):
                    workout = Activity()
                    workout.set_pace(int(self.new_pace))
                    workout.set_miles(float(self.newmiles))
                    workout.set_elevation(int(self.new_elev))
                    workout.set_hr(int(self.new_hr))
                    workout.set_zone(20)
                    workout.set_cals(int(self.newcals))
                    workout.set_name(self.new_name)
                    workout.set_date(self.new_date)
                    #workout.set_race(self.check_race)
                    if len(self.user_data) == 0:
                        self.user_data.insert(0, workout)
                        data_added = True
                    else:
                        self.user_data.append(workout)
                        data_added = True
                
                self.new_name = ""
                #add to total values
                select_query = "SELECT miles, activites FROM userProfile WHERE username = %s"
                self.cursor.execute(select_query, (self.current_username,))
                result = self.cursor.fetchone()  # Fetch one row (tuple)

                current_miles = float(result[0])
                current_activities = int(result[1])
                try:
                    # Convert user input to integer and add to miles_ran_num
                        if self.newmiles != "":
                            miles_to_add = float(self.newmiles)  # Convert to float
                            self.miles_ran_num += miles_to_add  # Update the total miles
                            current_miles += miles_to_add
                        if self.newcals != "":
                            cals_to_add = int(self.newcals)
                            self.calsburned += cals_to_add
                        if self.new_elev != "":
                            elev_to_add = int(self.new_elev)
                            self.elev += elev_to_add
                        current_activities += 1
                        # Update the database with new values
                        update_query = "UPDATE userProfile SET miles = %s, activites = %s WHERE username = %s"
                        self.cursor.execute(update_query, (current_miles, current_activities, self.current_username))
                        self.conn.commit()
                        print("database updated")
                except ValueError:
                    # If conversion to int fails, handle it here
                    messagebox.showerror("Invalid Input", "Please enter a valid number for miles.")