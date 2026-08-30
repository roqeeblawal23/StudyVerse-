import json
import random
import time


# ==========================================
# DATA STORAGE
# ==========================================

DATA_FILE = "studyverse_v2_data.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

            if not isinstance(data, dict) or "users" not in data:
                return {"users": {}}

            return data

    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": {}}


database = load_data()


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(database, file, indent=4)


# ==========================================
# USER DATA
# ==========================================

def create_user(username, email, password, display_name):

    return {
        "username": username,
        "email": email,
        "password": password,
        "name": display_name,

        "homework": [],
        "study_plans": [],
        "exams": [],
        "todo": [],
        "notes": [],

        "timetable": {
            "Monday": "Not Set",
            "Tuesday": "Not Set",
            "Wednesday": "Not Set",
            "Thursday": "Not Set",
            "Friday": "Not Set",
            "Saturday": "Not Set",
            "Sunday": "Not Set"
        },

        "attendance": {
            "present": 0,
            "absent": 0
        },

        "streak": 0,
        "last_study_date": None,
        "quiz_questions": []
    }


# ==========================================
# ACCOUNT LOGIC
# ==========================================

def create_account(username, email, password, confirm_password, display_name):

    username = username.strip()
    email = email.strip()
    display_name = display_name.strip()

    if not username:
        return False, "Username cannot be empty."

    if username in database["users"]:
        return False, "Username already exists."

    if "@" not in email or "." not in email:
        return False, "Invalid email address."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if password != confirm_password:
        return False, "Passwords do not match."

    database["users"][username] = create_user(
        username,
        email,
        password,
        display_name
    )

    save_data()

    return True, "Account created successfully!"


def authenticate_user(username, password):

    username = username.strip()

    if username not in database["users"]:
        return False, None

    user = database["users"][username]

    if user["password"] != password:
        return False, None

    return True, user


# ==========================================
# HOMEWORK LOGIC
# ==========================================

def add_homework(user, task):

    task = task.strip()

    if not task:
        return False, "Homework cannot be empty."

    user["homework"].append({
        "task": task,
        "status": "Not Done"
    })

    save_data()

    return True, "Homework added successfully."


def mark_homework_done(user, index):

    if 0 <= index < len(user["homework"]):

        user["homework"][index]["status"] = "Done"

        save_data()

        return True, "Homework marked as done."

    return False, "Invalid homework number."


def delete_homework(user, index):

    if 0 <= index < len(user["homework"]):

        deleted = user["homework"].pop(index)

        save_data()

        return True, f"Deleted '{deleted['task']}' successfully."

    return False, "Invalid homework number."


# ==========================================
# TO-DO LOGIC
# ==========================================

def add_todo(user, task):

    task = task.strip()

    if not task:
        return False, "Task cannot be empty."

    user["todo"].append({
        "task": task,
        "status": "Pending"
    })

    save_data()

    return True, "Task added successfully."


def complete_todo(user, index):

    if 0 <= index < len(user["todo"]):

        user["todo"][index]["status"] = "Done"

        save_data()

        return True, "Task completed."

    return False, "Invalid task number."


def delete_todo(user, index):

    if 0 <= index < len(user["todo"]):

        user["todo"].pop(index)

        save_data()

        return True, "Task deleted."

    return False, "Invalid task number."


# ==========================================
# NOTES LOGIC
# ==========================================

def add_note(user, note):

    note = note.strip()

    if not note:
        return False, "Note cannot be empty."

    user["notes"].append(note)

    save_data()

    return True, "Note saved successfully."


def delete_note(user, index):

    if 0 <= index < len(user["notes"]):

        user["notes"].pop(index)

        save_data()

        return True, "Note deleted."

    return False, "Invalid note number."


# ==========================================
# MOTIVATIONAL QUOTES
# ==========================================

def get_motivational_quote():

    quotes = [
        "Small progress is still progress.",
        "Consistency beats talent.",
        "Dream big, code harder!",
        "Your future is built by what you do today.",
        "Keep learning. Keep building. Keep improving.",
        "One step at a time."
    ]

    return random.choice(quotes)
 
# ==========================================
# KIVY GUI FUNCTIONS
# ==========================================

def login_user(username, password):

    username = username.strip()
    password = password.strip()

    if username not in database["users"]:
        return False, "Wrong username or password."

    user = database["users"][username]

    if user["password"] != password:
        return False, "Wrong username or password."

    return True, user


def create_account(username, email, password, confirm_password, display_name):

    username = username.strip()
    email = email.strip()
    password = password.strip()
    confirm_password = confirm_password.strip()
    display_name = display_name.strip()

    if not username:
        return False, "Username cannot be empty."

    if username in database["users"]:
        return False, "Username already exists."

    if "@" not in email or "." not in email:
        return False, "Invalid email address."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if password != confirm_password:
        return False, "Passwords do not match."

    if not display_name:
        display_name = "Student"

    database["users"][username] = create_user(
        username,
        email,
        password,
        display_name
    )

    save_data()

    return True, "Account created successfully!"