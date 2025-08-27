import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Ninjago2!",
        database = "vulcanTracker"
    )

def get_user_info(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM userProfile WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM userProfile")
    results = cursor.fetchall()
    conn.close()
    return results



def insert_user(fname, lname, username, password, age):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO signup (fname, lname, username, password, age) VALUES (%s, %s, %s, %s, %s)",
        (fname, lname, username, password, age)
    )
    conn.commit()
    conn.close()

def update_user_profile(username, miles, activities):
    conn = get_connection()
    cursor = conn.curosr()
    cursor.execute(
        "UPDATE userProfile SET miles = %s, activites = %s WHERE username = %s",
        (miles, activities, username)
    )
    conn.commit()
    conn.close()

def insert_activity(username, name, miles, calories, elevation, hr, pace, zone, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO activities
        (username, name, miles, calories, elevation, hr, pace, zone, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (username, name, miles, calories, elevation, hr, pace, zone, date)
    )
    conn.commit()
    conn.close()

def get_activity_by_name(username, name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # returns dict instead of tuple
    cursor.execute(
        "SELECT * FROM activities WHERE username = %s AND name = %s",
        (username, name)
    )
    row = cursor.fetchone()
    conn.close()
    return row
