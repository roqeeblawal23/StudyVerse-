import json
import random
import time

# ==========================================
# DATA STORAGE INITIALIZATION
# ==========================================
def load_data():
    try:
        with open("studyverse_data.json", "r") as file:
            data = json.load(file)
            # Safe-check: If the file exists but lacks our multi-user structure, fix it on the fly
            if not isinstance(data, dict) or "users" not in data:
                return {"users": {}}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Base database structure to hold multiple users if no file exists
        return {"users": {}}

def save_data(database):
    with open("studyverse_data.json", "w") as file:
        json.dump(database, file, indent=4)

# Load the database right at the beginning
database = load_data()

print("--- Welcome to StudyVerse ---")
name = input("Enter your name: ").strip()

# ==========================================
# MAIN ACCOUNT LOOP
# ==========================================
while True:
    print("\n=== ACCOUNT SYSTEM ===")
    print("1. Sign Up")
    print("2. Login")
    print("3. Exit")
    
    account_choice = input("Choose: ").strip()
    
    if account_choice == "1":
        reg_user = input("Create username: ").strip()
        reg_email = input("Enter email: ").strip()
        reg_password = input("Create password: ").strip()
        
        if reg_user in database["users"]:
            print("Username already exists! Try logging in.")
        elif reg_user == "":
            print("Username cannot be blank.")
        else:
            # Create a complete structural template for this specific profile
            database["users"][reg_user] = {
                "username": reg_user,
                "email": reg_email,
                "password": reg_password,
                "homework": [],
                "study_plans": [],
                "todo": [],
                "exams": [],
                "notes": [],
                "quiz_questions": [],
                "streak": 0,
                "attendance": {"present": 0, "absent": 0},
                "timetable": {
                    "Monday": "Not Set", 
                    "Tuesday": "Not Set", 
                    "Wednesday": "Not Set", 
                    "Thursday": "Not Set", 
                    "Friday": "Not Set"
                }
            }
            save_data(database)
            print("Account created successfully!")
        
    elif account_choice == "2":
        login_user = input("Username: ").strip()
        login_password = input("Password: ").strip()
        
        if login_user in database["users"] and database["users"][login_user]["password"] == login_password:
            print("Login successful!")
            
            # --- POPULATE RUNTIME ENVIRONMENT FROM JSON BACKEND ---
            current_user_data = database["users"][login_user]
            
            name = current_user_data["username"]
            homework_list = current_user_data.get("homework", [])
            study_plans = current_user_data.get("study_plans", [])
            todo_list = current_user_data.get("todo", [])
            exams = current_user_data.get("exams", [])
            notes = current_user_data.get("notes", [])
            quiz_questions = current_user_data.get("quiz_questions", [])
            study_streak = current_user_data.get("streak", 0)
            
            attendance = current_user_data.get("attendance", {"present": 0, "absent": 0})
            present_days = attendance.get("present", 0)
            absent_days = attendance.get("absent", 0)
            
            timetable = current_user_data.get("timetable", {
                "Monday": "Not Set", "Tuesday": "Not Set", "Wednesday": "Not Set", "Thursday": "Not Set", "Friday": "Not Set"
            })
            
            # ==========================================
            # MAIN STUDENT DASHBOARD LOOP
            # ==========================================
            while True:
                print(f"\n=== StudyVerse Dashboard | User: {name.upper()} ===")
                print("1. Add Homework")
                print("2. View & Delete Homework")
                print("3. Add Study Plan")
                print("4. View Study Plans")
                print("5. GPA Checker")
                print("6. Mark Homework as Done")
                print("7. Statistics")
                print("8. Edit Homework")
                print("9. Delete Study Plan")
                print("10. Search Homework")
                print("11. Add To-Do Task")
                print("12. View To-Do List")
                print("13. Add Exam Countdown")
                print("14. View Upcoming Exams")
                print("15. Multi-Subject GPA Calculator")
                print("16. Daily Study Streak")
                print("17. Save Data")
                print("18. Motivational Quote")
                print("19. Add Note")
                print("20. View Notes")
                print("21. Mark Attendance (Present)")
                print("22. Mark Attendance (Absent)")
                print("23. View Attendance Statistics")
                print("24. Add Quiz Questions")
                print("25. Take Quiz")
                print("26. Homework Reminder")
                print("27. Study Timer")
                print("28. Change Password")
                print("29. Dashboard Summary")
                print("30. Profile Editor")
                print("31. Calculator")
                print("32. CGPA Calculator")
                print("33. Timetable Manager")
                print("34. Alarm & Study Scheduler")
                print("35. Exit Dashboard")
                
                choice = input("Choose: ").strip()
                
                if choice == "1":
                    hw = input("Enter homework: ")
                    homework_list.append({"task": hw, "status": "Not Done"})
                    print("Homework added successfully!")
                    
                elif choice == "2":
                    print("\n--- HOMEWORK LIST ---")
                    if not homework_list:
                        print("No homework added yet.")
                    for idx, h in enumerate(homework_list, 1):
                        print(f"{idx} - {h['task']} - {h['status']}")
                    del_choice = input("Enter number to delete (or press Enter to skip): ")
                    if del_choice.isdigit():
                        del_idx = int(del_choice) - 1
                        if 0 <= del_idx < len(homework_list):
                            homework_list.pop(del_idx)
                            print("Deleted successfully!")
                            
                elif choice == "3":
                    subject = input("Enter subject: ")
                    duration = input("Enter study time: ")
                    study_plans.append({"subject": subject, "time": duration})
                    print("Study plan added!")
                    
                elif choice == "4":
                    print("\n--- STUDY PLANS ---")
                    for idx, p in enumerate(study_plans, 1):
                        print(f"{idx} - {p['subject']} - {p['time']}")
                        
                elif choice == "5":
                    try:
                        score = float(input("Enter your score: "))
                        if score >= 70: 
                            print("Grade: A")
                        elif score >= 60: 
                            print("Grade: B")
                        elif score >= 50: 
                            print("Grade: C")
                        else: 
                            print("Grade: F")
                    except ValueError:
                        print("Invalid input!")
                        
                elif choice == "6":
                    for idx, h in enumerate(homework_list, 1):
                        print(f"{idx} - {h['task']}")
                    hw_num = input("Enter homework number: ")
                    if hw_num.isdigit():
                        idx = int(hw_num) - 1
                        if 0 <= idx < len(homework_list):
                            homework_list[idx]["status"] = "Done"
                            print("Homework marked as done!")
                            
                elif choice == "7":
                    total_hw = len(homework_list)
                    done_hw = sum(1 for h in homework_list if h["status"] == "Done")
                    rem_hw = total_hw - done_hw
                    comp_rate = (done_hw / total_hw * 100) if total_hw > 0 else 0.0
                    print(f"\n=== STATISTICS ===\nTotal Homework: {total_hw}\nHomework Done: {done_hw}\nRemaining: {rem_hw}\nCompletion: {comp_rate:.1f} %")
                    
                elif choice == "8":
                    for idx, h in enumerate(homework_list, 1):
                        print(f"{idx} - {h['task']}")
                    edit_choice = input("Enter homework number to edit: ")
                    if edit_choice.isdigit():
                        idx = int(edit_choice) - 1
                        if 0 <= idx < len(homework_list):
                            new_hw = input("Enter new homework details: ")
                            homework_list[idx]["task"] = new_hw
                            print("Updated successfully!")
                            
                elif choice == "9":
                    for idx, p in enumerate(study_plans, 1):
                        print(f"{idx} - {p['subject']} - {p['time']}")
                    del_p = input("Enter study plan number to delete: ")
                    if del_p.isdigit():
                        idx = int(del_p) - 1
                        if 0 <= idx < len(study_plans):
                            study_plans.pop(idx)
                            print("Study plan deleted!")
                            
                elif choice == "10":
                    search_term = input("Enter homework name to search: ").lower()
                    for idx, h in enumerate(homework_list, 1):
                        if search_term in h["task"].lower():
                            print(f"{idx} - {h['task']} - {h['status']}")
                            
                elif choice == "11":
                    task = input("Enter task: ")
                    todo_list.append(task)
                    print("Task added successfully!")
                    
                elif choice == "12":
                    print("\n--- TO-DO LIST ---")
                    for idx, t in enumerate(todo_list, 1):
                        print(f"{idx} - {t}")
                        
                elif choice == "13":
                    ex_subject = input("Enter exam subject: ")
                    days_left = input("How many days left? ")
                    exams.append({"subject": ex_subject, "days": days_left})
                    print("Exam added!")
                    
                elif choice == "14":
                    print("\n--- UPCOMING EXAMS ---")
                    for idx, e in enumerate(exams, 1):
                        print(f"{idx} - {e['subject']} - {e['days']} days left")
                        
                elif choice == "15":
                    try:
                        num_sub = int(input("How many subjects? "))
                        total_score = 0
                        for i in range(num_sub):
                            total_score += float(input(f"Enter score for subject {i+1}: "))
                        avg = total_score / num_sub if num_sub > 0 else 0
                        print(f"Average score: {avg:.1f}")
                        if avg >= 70: 
                            print("Overall Grade: A")
                        else: 
                            print("Overall Grade: Passed")
                    except ValueError:
                        print("Invalid input!")
                        
                elif choice == "16":
                    status = input("Did you study today? (yes/no): ").lower()
                    if status == "yes":
                        study_streak += 1
                    else:
                        study_streak = 0
                    print(f"Current Study Streak: {study_streak} days")
                    
                elif choice == "17":
                    # Pack runtime values back into core database layout
                    database["users"][login_user]["homework"] = homework_list
                    database["users"][login_user]["study_plans"] = study_plans
                    database["users"][login_user]["todo"] = todo_list
                    database["users"][login_user]["exams"] = exams
                    database["users"][login_user]["notes"] = notes
                    database["users"][login_user]["quiz_questions"] = quiz_questions
                    database["users"][login_user]["streak"] = study_streak
                    database["users"][login_user]["attendance"] = {"present": present_days, "absent": absent_days}
                    database["users"][login_user]["timetable"] = timetable
                    
                    save_data(database)
                    print("Data saved successfully!")
                    
                elif choice == "18":
                    quotes = ["Small progress is still progress.", "Consistency beats talent.", "Dream big, code harder!"]
                    print(f"\nMotivational Quote:\n{random.choice(quotes)}")
                    
                elif choice == "19":
                    note_input = input("Write note: ")
                    notes.append(note_input)
                    print("Note saved!")
                    
                elif choice == "20":
                    print("\n--- NOTES ---")
                    for idx, n in enumerate(notes, 1):
                        print(f"{idx} - {n}")
                        
                elif choice == "21":
                    present_days += 1
                    print(f"Present days: {present_days}")
                    
                elif choice == "22":
                    absent_days += 1
                    print(f"Absent days: {absent_days}")
                    
                elif choice == "23":
                    total_days = present_days + absent_days
                    rate = (present_days / total_days * 100) if total_days > 0 else 0.0
                    print(f"Present: {present_days}\nAbsent: {absent_days}\nAttendance: {rate:.1f} %")
                    
                elif choice == "24":
                    q = input("Enter question: ")
                    a = input("Enter answer: ")
                    quiz_questions.append({"question": q, "answer": a})
                    print("Question saved!")
                    
                elif choice == "25":
                    if not quiz_questions:
                        print("No questions added yet!")
                    else:
                        score = 0
                        for q in quiz_questions:
                            print(q["question"])
                            ans = input("Answer: ")
                            if ans.lower() == q["answer"].lower():
                                score += 1
                        print(f"Score: {score} / {len(quiz_questions)}")
                        
                elif choice == "26":
                    print("\n--- REMINDERS ---")
                    for h in homework_list:
                        if h["status"] == "Not Done":
                            print(f"Don't forget: {h['task']}")
                            
                elif choice == "27":
                    try:
                        secs = int(input("Enter seconds: "))
                        for i in range(secs, 0, -1):
                            print(i)
                            time.sleep(1)
                        print("Study session completed!")
                    except ValueError:
                        print("Please enter an integer.")
                        
                elif choice == "28":
                    old_pw = input("Enter old password: ")
                    if old_pw == database["users"][login_user]["password"]:
                        new_pw = input("Enter new password: ")
                        conf_pw = input("Confirm new password: ")
                        if new_pw == conf_pw:
                            database["users"][login_user]["password"] = new_pw
                            save_data(database)
                            print("Password changed and saved!")
                        else:
                            print("Passwords do not match!")
                    else:
                        print("Incorrect old password.")
                        
                elif choice == "29":
                    total_hw = len(homework_list)
                    done_hw = sum(1 for h in homework_list if h["status"] == "Done")
                    hw_rate = (done_hw / total_hw * 100) if total_hw > 0 else 0.0
                    total_days = present_days + absent_days
                    att_rate = (present_days / total_days * 100) if total_days > 0 else 0.0
                    print(f"\n=== DASHBOARD SUMMARY ===\nName: {name}\nUsername: {login_user}\nHomework: {total_hw}\nHomework Done: {done_hw}\nStudy Plans: {len(study_plans)}\nTo-Do Tasks: {len(todo_list)}\nExams: {len(exams)}\nNotes: {len(notes)}\nQuiz Questions: {len(quiz_questions)}\nStudy Streak: {study_streak}\nAttendance: {att_rate:.1f} %\nHomework Completion: {hw_rate:.1f} %")
                    
                elif choice == "30":
                    print("\n--- Profile Editor ---")
                    print(f"Current Name: {name}\nCurrent Username: {login_user}")
                    confirm = input("Do you want to update your profile screen name? (yes/no): ").lower()
                    if confirm == "yes":
                        name = input("Enter new display name: ")
                        print("Display profile name updated inside dashboard!")
                    else:
                        print("Profile changes cancelled.")
                        
                elif choice == "31":
                    print("\n--- StudyVerse Calculator ---")
                    try:
                        num1 = float(input("Enter first number: "))
                        operation = input("Enter operation (+, -, *, /): ")
                        num2 = float(input("Enter second number: "))
                        if operation == "+": 
                            print(f"Result: {num1 + num2}")
                        elif operation == "-": 
                            print(f"Result: {num1 - num2}")
                        elif operation == "*": 
                            print(f"Result: {num1 * num2}")
                        elif operation == "/":
                            if num2 == 0: 
                                print("Error: Cannot divide by zero!")
                            else: 
                                print(f"Result: {num1 / num2}")
                        else: 
                            print("Invalid operation symbol!")
                    except ValueError:
                        print("Invalid input! Numbers only.")
                        
                elif choice == "32":
                    print(f"\n--- StudyVerse CGPA Calculator | User: {name.upper()} ---")
                    try:
                        num_semesters = int(input("How many semesters? "))
                        if num_semesters > 0:
                            total_gpa = 0.0
                            for i in range(1, num_semesters + 1):
                                gpa = float(input(f"Enter GPA for Semester {i}: "))
                                total_gpa += gpa
                            cgpa = total_gpa / num_semesters
                            print(f"\nYour Cumulative GPA (CGPA): {cgpa:.2f}")
                            if cgpa >= 4.5: 
                                print("Excellent! First Class Standing. 🚀")
                            elif cgpa >= 3.5: 
                                print("Very good performance!")
                            else: 
                                print("Keep pushing to scale it higher!")
                    except ValueError:
                        print("Invalid input!")
                        
                elif choice == "33":
                    print(f"\n--- StudyVerse Timetable Manager | User: {name.upper()} ---")
                    print("1. View Weekly Timetable\n2. Update a Day's Schedule")
                    sub_choice = input("Choose (1 or 2): ")
                    if sub_choice == "1":
                        for day, task in timetable.items():
                            print(f"🗓 {day}: {task}")
                    elif sub_choice == "2":
                        day_to_update = input("Enter day (e.g., Monday): ").strip().capitalize()
                        if day_to_update in timetable:
                            timetable[day_to_update] = input(f"What are you studying on {day_to_update}?: ")
                            print("Success! Schedule updated.")
                            
                elif choice == "34":
                    print("\n--- StudyVerse Scheduler ---")
                    try:
                        minutes = int(input("Enter study time in minutes: "))
                        seconds = minutes * 60
                        print(f"Timer started for {minutes} minutes!")
                        while seconds > 0:
                            print(f"Time remaining: {seconds} seconds", end="\r")
                            time.sleep(1)
                            seconds -= 1
                        print("\n⏰ BZZZ! Time's up! Take a break, Product Lead! 🚀")
                    except ValueError:
                        print("Invalid number input.")
                        
                elif choice == "35":
                    print("Logging out of dashboard...")
                    break
                    
                else:
                    print("Invalid option selection.")
                    
        else:
            print("Login failed. Wrong username or password.")
            
    elif account_choice == "3":
        print("Goodbye!")
        break
