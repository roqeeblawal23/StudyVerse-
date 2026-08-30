from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock

import studyverse_logic


class StudyVerseApp(App):

    def build(self):
        self.current_user = None
        self.root_layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        self.show_welcome()

        return self.root_layout

    # ==========================================
    # BASIC UI HELPERS
    # ==========================================

    def clear_screen(self):
        self.root_layout.clear_widgets()

    def add_title(self, text):
        title = Label(
            text=text,
            font_size=26,
            bold=True,
            size_hint_y=None,
            height=60
        )
        self.root_layout.add_widget(title)

    def add_button(self, text, callback):
        button = Button(
            text=text,
            size_hint_y=None,
            height=55
        )
        button.bind(on_press=callback)
        self.root_layout.add_widget(button)

    def show_message(self, title, message):
        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        content.add_widget(
            Label(text=message)
        )

        close_button = Button(
            text="OK",
            size_hint_y=None,
            height=50
        )

        content.add_widget(close_button)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.85, 0.45)
        )

        close_button.bind(
            on_press=popup.dismiss
        )

        popup.open()

    # ==========================================
    # WELCOME
    # ==========================================

    def show_welcome(self):
        self.clear_screen()

        self.add_title("WELCOME TO STUDYVERSE")

        self.add_button(
            "LOGIN",
            self.show_login
        )

        self.add_button(
            "SIGN UP",
            self.show_signup
        )

    # ==========================================
    # LOGIN
    # ==========================================

    def show_login(self, instance=None):
        self.clear_screen()

        self.add_title("STUDYVERSE LOGIN")

        self.username_input = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.root_layout.add_widget(
            self.username_input
        )

        self.root_layout.add_widget(
            self.password_input
        )

        self.add_button(
            "LOGIN",
            self.login_user
        )

        self.add_button(
            "BACK",
            lambda x: self.show_welcome()
        )

    def login_user(self, instance):

        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        database = studyverse_logic.database

        if username not in database["users"]:
            self.show_message(
                "Login Failed",
                "Wrong username or password."
            )
            return

        user = database["users"][username]

        if user["password"] != password:
            self.show_message(
                "Login Failed",
                "Wrong username or password."
            )
            return

        self.current_user = user

        self.show_dashboard()

    # ==========================================
    # SIGN UP
    # ==========================================

    def show_signup(self, instance=None):
        self.clear_screen()

        self.add_title("CREATE STUDYVERSE ACCOUNT")

        self.name_input = TextInput(
            hint_text="Display Name",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.signup_username = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.signup_email = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.signup_password = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.signup_confirm = TextInput(
            hint_text="Confirm Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.root_layout.add_widget(self.name_input)
        self.root_layout.add_widget(self.signup_username)
        self.root_layout.add_widget(self.signup_email)
        self.root_layout.add_widget(self.signup_password)
        self.root_layout.add_widget(self.signup_confirm)

        self.add_button(
            "CREATE ACCOUNT",
            self.create_account
        )

        self.add_button(
            "BACK",
            lambda x: self.show_welcome()
        )

    def create_account(self, instance):

        name = self.name_input.text.strip()
        username = self.signup_username.text.strip()
        email = self.signup_email.text.strip()
        password = self.signup_password.text
        confirm = self.signup_confirm.text

        database = studyverse_logic.database

        if not name:
            self.show_message(
                "Error",
                "Enter your display name."
            )
            return

        if not username:
            self.show_message(
                "Error",
                "Username cannot be empty."
            )
            return

        if username in database["users"]:
            self.show_message(
                "Error",
                "Username already exists."
            )
            return

        if "@" not in email or "." not in email:
            self.show_message(
                "Error",
                "Enter a valid email."
            )
            return

        if len(password) < 8:
            self.show_message(
                "Error",
                "Password must be at least 8 characters."
            )
            return

        if password != confirm:
            self.show_message(
                "Error",
                "Passwords do not match."
            )
            return

        new_user = studyverse_logic.create_user(
            username,
            email,
            password,
            name
        )

        database["users"][username] = new_user

        studyverse_logic.save_data()

        self.current_user = new_user

        self.show_message(
            "Success",
            "StudyVerse account created successfully!"
        )

        Clock.schedule_once(
            lambda dt: self.show_dashboard(),
            0.5
        )

    # ==========================================
    # DASHBOARD
    # ==========================================

    def show_dashboard(self, instance=None):
        self.clear_screen()

        name = self.current_user["name"]

        self.add_title(
            "STUDYVERSE DASHBOARD"
        )

        self.root_layout.add_widget(
            Label(
                text=f"Welcome, {name} 👋",
                size_hint_y=None,
                height=45
            )
        )

        self.add_button(
            "📚 ACADEMICS",
            self.show_academics
        )

        self.add_button(
            "✅ PRODUCTIVITY",
            self.show_productivity
        )

        self.add_button(
            "📊 PERFORMANCE",
            self.show_performance
        )

        self.add_button(
            "🧠 LEARNING",
            self.show_learning
        )

        self.add_button(
            "⏱ STUDY TOOLS",
            self.show_study_tools
        )

        self.add_button(
            "👤 PROFILE",
            self.show_profile
        )

        self.add_button(
            "📋 DASHBOARD SUMMARY",
            self.show_summary
        )

        self.add_button(
            "🚪 LOGOUT",
            self.logout
        )

    # ==========================================
    # ACADEMICS
    # ==========================================

    def show_academics(self, instance=None):
        self.clear_screen()

        self.add_title("📚 ACADEMICS")

        self.add_button(
            "📚 HOMEWORK",
            self.show_homework
        )

        self.add_button(
            "📖 STUDY PLANS",
            self.show_study_plans
        )

        self.add_button(
            "🎓 GPA CALCULATOR",
            self.show_gpa
        )

        self.add_button(
            "📝 EXAMS",
            self.show_exams
        )

        self.add_button(
            "BACK",
            self.show_dashboard
        )

    # ==========================================
    # HOMEWORK
    # ==========================================

    def show_homework(self, instance=None):
        self.clear_screen()

        self.add_title("📚 HOMEWORK")

        homework = self.current_user["homework"]

        if not homework:
            self.root_layout.add_widget(
                Label(
                    text="No homework yet.",
                    size_hint_y=None,
                    height=50
                )
            )
        else:
            for index, item in enumerate(homework):

                text = (
                    f"{index + 1}. "
                    f"{item['task']} - "
                    f"{item['status']}"
                )

                self.root_layout.add_widget(
                    Label(
                        text=text,
                        size_hint_y=None,
                        height=45
                    )
                )

        self.add_button(
            "ADD HOMEWORK",
            self.add_homework_popup
        )

        self.add_button(
            "BACK",
            self.show_academics
        )

    def add_homework_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        text_input = TextInput(
            hint_text="Enter homework",
            multiline=False
        )

        content.add_widget(text_input)

        button = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(button)

        popup = Popup(
            title="Add Homework",
            content=content,
            size_hint=(0.85, 0.4)
        )

        def save_homework(instance):

            task = text_input.text.strip()

            if not task:
                return

            self.current_user["homework"].append({
                "task": task,
                "status": "Not Done"
            })

            studyverse_logic.save_data()

            popup.dismiss()
            self.show_homework()

        button.bind(on_press=save_homework)

        popup.open()

    # ==========================================
    # STUDY PLANS
    # ==========================================

    def show_study_plans(self, instance=None):
        self.clear_screen()

        self.add_title("📖 STUDY PLANS")

        plans = self.current_user["study_plans"]

        if not plans:
            self.root_layout.add_widget(
                Label(
                    text="No study plans yet.",
                    size_hint_y=None,
                    height=50
                )
            )

        for index, plan in enumerate(plans, 1):

            self.root_layout.add_widget(
                Label(
                    text=f"{index}. {plan['subject']} - {plan['time']}",
                    size_hint_y=None,
                    height=45
                )
            )

        self.add_button(
            "ADD STUDY PLAN",
            self.add_study_plan_popup
        )

        self.add_button(
            "BACK",
            self.show_academics
        )

    def add_study_plan_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        subject = TextInput(
            hint_text="Subject",
            multiline=False
        )

        study_time = TextInput(
            hint_text="Study time",
            multiline=False
        )

        save = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(subject)
        content.add_widget(study_time)
        content.add_widget(save)

        popup = Popup(
            title="Add Study Plan",
            content=content,
            size_hint=(0.85, 0.5)
        )

        def save_plan(instance):

            if not subject.text.strip():
                return

            if not study_time.text.strip():
                return

            self.current_user["study_plans"].append({
                "subject": subject.text.strip(),
                "time": study_time.text.strip()
            })

            studyverse_logic.save_data()

            popup.dismiss()

            self.show_study_plans()

        save.bind(on_press=save_plan)

        popup.open()

    # ==========================================
    # GPA
    # ==========================================

    def show_gpa(self, instance=None):

        self.clear_screen()

        self.add_title("🎓 GPA CALCULATOR")

        self.gpa_subjects = TextInput(
            hint_text="Number of subjects",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=50
        )

        self.root_layout.add_widget(
            self.gpa_subjects
        )

        self.add_button(
            "CALCULATE",
            self.calculate_gpa
        )

        self.add_button(
            "BACK",
            self.show_academics
        )

    def calculate_gpa(self, instance):

        try:
            count = int(
                self.gpa_subjects.text
            )

            if count <= 0:
                raise ValueError

        except ValueError:
            self.show_message(
                "Error",
                "Enter a valid number of subjects."
            )
            return

        self.gpa_inputs = []

        self.clear_screen()

        self.add_title(
            "ENTER SUBJECT SCORES"
        )

        for i in range(count):

            field = TextInput(
                hint_text=f"Subject {i + 1} score",
                multiline=False,
                input_filter="float",
                size_hint_y=None,
                height=50
            )

            self.gpa_inputs.append(field)

            self.root_layout.add_widget(field)

        self.add_button(
            "CALCULATE GPA",
            self.finish_gpa
        )

    def finish_gpa(self, instance):

        try:
            scores = [
                float(field.text)
                for field in self.gpa_inputs
            ]

            if any(
                score < 0 or score > 100
                for score in scores
            ):
                raise ValueError

            average = sum(scores) / len(scores)

        except (ValueError, ZeroDivisionError):

            self.show_message(
                "Error",
                "Enter valid scores between 0 and 100."
            )
            return

        if average >= 70:
            grade = "A"
        elif average >= 60:
            grade = "B"
        elif average >= 50:
            grade = "C"
        elif average >= 45:
            grade = "D"
        elif average >= 40:
            grade = "E"
        else:
            grade = "F"

        self.show_message(
            "GPA Result",
            f"Average: {average:.2f}\nGrade: {grade}"
        )

        self.show_academics()

    # ==========================================
    # EXAMS
    # ==========================================

    def show_exams(self, instance=None):

        self.clear_screen()

        self.add_title("📝 EXAMS")

        exams = self.current_user["exams"]

        if not exams:
            self.root_layout.add_widget(
                Label(
                    text="No upcoming exams.",
                    size_hint_y=None,
                    height=50
                )
            )

        for index, exam in enumerate(exams, 1):

            self.root_layout.add_widget(
                Label(
                    text=f"{index}. {exam['subject']} - {exam['days']} days left",
                    size_hint_y=None,
                    height=45
                )
            )

        self.add_button(
            "ADD EXAM",
            self.add_exam_popup
        )

        self.add_button(
            "BACK",
            self.show_academics
        )

    def add_exam_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        subject = TextInput(
            hint_text="Exam subject",
            multiline=False
        )

        days = TextInput(
            hint_text="Days left",
            multiline=False,
            input_filter="int"
        )

        save = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(subject)
        content.add_widget(days)
        content.add_widget(save)

        popup = Popup(
            title="Add Exam",
            content=content,
            size_hint=(0.85, 0.5)
        )

        def save_exam(instance):

            try:
                day_count = int(days.text)

                if day_count < 0:
                    raise ValueError

            except ValueError:
                return

            if not subject.text.strip():
                return

            self.current_user["exams"].append({
                "subject": subject.text.strip(),
                "days": day_count
            })

            studyverse_logic.save_data()

            popup.dismiss()

            self.show_exams()

        save.bind(on_press=save_exam)

        popup.open()

    # ==========================================
    # PRODUCTIVITY
    # ==========================================

    def show_productivity(self, instance=None):

        self.clear_screen()

        self.add_title("✅ PRODUCTIVITY")

        self.add_button(
            "✅ TO-DO",
            self.show_todo
        )

        self.add_button(
            "📝 NOTES",
            self.show_notes
        )

        self.add_button(
            "📅 TIMETABLE",
            self.show_timetable
        )

        self.add_button(
            "BACK",
            self.show_dashboard
        )

    # ==========================================
    # TODO
    # ==========================================

    def show_todo(self, instance=None):

        self.clear_screen()

        self.add_title("✅ TO-DO LIST")

        tasks = self.current_user["todo"]

        for index, task in enumerate(tasks, 1):

            self.root_layout.add_widget(
                Label(
                    text=f"{index}. {task['task']} - {task['status']}",
                    size_hint_y=None,
                    height=45
                )
            )

        if not tasks:
            self.root_layout.add_widget(
                Label(
                    text="No tasks yet.",
                    size_hint_y=None,
                    height=50
                )
            )

        self.add_button(
            "ADD TASK",
            self.add_todo_popup
        )

        self.add_button(
            "BACK",
            self.show_productivity
        )

    def add_todo_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        field = TextInput(
            hint_text="Enter task",
            multiline=False
        )

        save = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(field)
        content.add_widget(save)

        popup = Popup(
            title="Add To-Do",
            content=content,
            size_hint=(0.85, 0.4)
        )

        def save_task(instance):

            task = field.text.strip()

            if not task:
                return

            self.current_user["todo"].append({
                "task": task,
                "status": "Pending"
            })

            studyverse_logic.save_data()

            popup.dismiss()

            self.show_todo()

        save.bind(on_press=save_task)

        popup.open()

    # ==========================================
    # NOTES
    # ==========================================

    def show_notes(self, instance=None):

        self.clear_screen()

        self.add_title("📝 NOTES")

        notes = self.current_user["notes"]

        if not notes:
            self.root_layout.add_widget(
                Label(
                    text="No notes yet.",
                    size_hint_y=None,
                    height=50
                )
            )

        for index, note in enumerate(notes, 1):

            self.root_layout.add_widget(
                Label(
                    text=f"{index}. {note}",
                    size_hint_y=None,
                    height=55
                )
            )

        self.add_button(
            "ADD NOTE",
            self.add_note_popup
        )

        self.add_button(
            "BACK",
            self.show_productivity
        )

    def add_note_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        field = TextInput(
            hint_text="Write your note",
            multiline=True
        )

        save = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(field)
        content.add_widget(save)

        popup = Popup(
            title="Add Note",
            content=content,
            size_hint=(0.9, 0.6)
        )

        def save_note(instance):

            note = field.text.strip()

            if not note:
                return

            self.current_user["notes"].append(note)

            studyverse_logic.save_data()

            popup.dismiss()

            self.show_notes()

        save.bind(on_press=save_note)

        popup.open()

    # ==========================================
    # TIMETABLE
    # ==========================================

    def show_timetable(self, instance=None):

        self.clear_screen()

        self.add_title("📅 TIMETABLE")

        for day, schedule in self.current_user["timetable"].items():

            self.root_layout.add_widget(
                Label(
                    text=f"{day}: {schedule}",
                    size_hint_y=None,
                    height=45
                )
            )

        self.add_button(
            "UPDATE TIMETABLE",
            self.update_timetable_popup
        )

        self.add_button(
            "BACK",
            self.show_productivity
        )

    def update_timetable_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        day = TextInput(
            hint_text="Day e.g. Monday",
            multiline=False
        )

        schedule = TextInput(
            hint_text="What are you studying?",
            multiline=False
        )

        save = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(day)
        content.add_widget(schedule)
        content.add_widget(save)

        popup = Popup(
            title="Update Timetable",
            content=content,
            size_hint=(0.85, 0.5)
        )

        def save_schedule(instance):

            selected_day = day.text.strip().capitalize()

            if selected_day not in self.current_user["timetable"]:
                return

            if not schedule.text.strip():
                return

            self.current_user["timetable"][selected_day] = (
                schedule.text.strip()
            )

            studyverse_logic.save_data()

            popup.dismiss()

            self.show_timetable()

        save.bind(on_press=save_schedule)

        popup.open()

    # ==========================================
    # PERFORMANCE
    # ==========================================

    def show_performance(self, instance=None):

        self.clear_screen()

        self.add_title("📊 PERFORMANCE")

        user = self.current_user

        homework_total = len(
            user["homework"]
        )

        homework_done = sum(
            1
            for item in user["homework"]
            if item["status"] == "Done"
        )

        todo_total = len(user["todo"])

        todo_done = sum(
            1
            for item in user["todo"]
            if item["status"] == "Done"
        )

        present = user["attendance"]["present"]
        absent = user["attendance"]["absent"]

        attendance_total = present + absent

        attendance_rate = (
            present / attendance_total * 100
            if attendance_total > 0
            else 0
        )

        self.root_layout.add_widget(
            Label(
                text=f"Homework: {homework_total}",
                size_hint_y=None,
                height=45
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"Homework Completed: {homework_done}",
                size_hint_y=None,
                height=45
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"To-Do Tasks: {todo_total}",
                size_hint_y=None,
                height=45
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"To-Do Completed: {todo_done}",
                size_hint_y=None,
                height=45
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"Attendance: {attendance_rate:.1f}%",
                size_hint_y=None,
                height=45
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"Study Streak: {user['streak']} days 🔥",
                size_hint_y=None,
                height=45
            )
        )

        self.add_button(
            "🏫 ATTENDANCE",
            self.show_attendance
        )

        self.add_button(
            "🔥 STUDY STREAK",
            self.show_streak
        )

        self.add_button(
            "BACK",
            self.show_dashboard
        )

    # ==========================================
    # ATTENDANCE
    # ==========================================

    def show_attendance(self, instance=None):

        self.clear_screen()

        self.add_title("🏫 ATTENDANCE")

        attendance = self.current_user["attendance"]

        present = attendance["present"]
        absent = attendance["absent"]

        total = present + absent

        rate = (
            present / total * 100
            if total > 0
            else 0
        )

        self.root_layout.add_widget(
            Label(
                text=f"Present: {present}",
                size_hint_y=None,
                height=50
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"Absent: {absent}",
                size_hint_y=None,
                height=50
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"Attendance Rate: {rate:.1f}%",
                size_hint_y=None,
                height=50
            )
        )

        self.add_button(
            "MARK PRESENT",
            self.mark_present
        )

        self.add_button(
            "MARK ABSENT",
            self.mark_absent
        )

        self.add_button(
            "BACK",
            self.show_performance
        )

    def mark_present(self, instance):

        self.current_user["attendance"]["present"] += 1

        studyverse_logic.save_data()

        self.show_attendance()

    def mark_absent(self, instance):

        self.current_user["attendance"]["absent"] += 1

        studyverse_logic.save_data()

        self.show_attendance()

    # ==========================================
    # STREAK
    # ==========================================

    def show_streak(self, instance=None):

        self.clear_screen()

        self.add_title("🔥 STUDY STREAK")

        self.root_layout.add_widget(
            Label(
                text=f"Current streak: "
                     f"{self.current_user['streak']} days 🔥",
                size_hint_y=None,
                height=60
            )
        )

        self.add_button(
            "I STUDIED TODAY",
            self.studied_today
        )

        self.add_button(
            "RESET STREAK",
            self.reset_streak
        )

        self.add_button(
            "BACK",
            self.show_performance
        )

    def studied_today(self, instance):

        self.current_user["streak"] += 1

        studyverse_logic.save_data()

        self.show_streak()

    def reset_streak(self, instance):

        self.current_user["streak"] = 0

        studyverse_logic.save_data()

        self.show_streak()

    # ==========================================
    # LEARNING / QUIZ
    # ==========================================

    def show_learning(self, instance=None):

        self.clear_screen()

        self.add_title("🧠 LEARNING")

        self.add_button(
            "🧠 QUIZ",
            self.show_quiz
        )

        self.add_button(
            "BACK",
            self.show_dashboard
        )

    def show_quiz(self, instance=None):

        self.clear_screen()

        self.add_title("🧠 QUIZ")

        questions = self.current_user["quiz_questions"]

        if not questions:

            self.root_layout.add_widget(
                Label(
                    text="No quiz questions yet.",
                    size_hint_y=None,
                    height=50
                )
            )

        for index, item in enumerate(questions, 1):

            self.root_layout.add_widget(
                Label(
                    text=f"{index}. {item['question']}",
                    size_hint_y=None,
                    height=50
                )
            )

        self.add_button(
            "ADD QUESTION",
            self.add_quiz_popup
        )

        self.add_button(
            "TAKE QUIZ",
            self.take_quiz
        )

        self.add_button(
            "BACK",
            self.show_learning
        )

    def add_quiz_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        question = TextInput(
            hint_text="Question",
            multiline=True
        )

        answer = TextInput(
            hint_text="Answer",
            multiline=False
        )

        save = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(question)
        content.add_widget(answer)
        content.add_widget(save)

        popup = Popup(
            title="Add Quiz Question",
            content=content,
            size_hint=(0.9, 0.6)
        )

        def save_question(instance):

            q = question.text.strip()
            a = answer.text.strip()

            if not q or not a:
                return

            self.current_user["quiz_questions"].append({
                "question": q,
                "answer": a
            })

            studyverse_logic.save_data()

            popup.dismiss()

            self.show_quiz()

        save.bind(on_press=save_question)

        popup.open()

    def take_quiz(self, instance):

        questions = self.current_user["quiz_questions"]

        if not questions:
            self.show_message(
                "Quiz",
                "No quiz questions available."
            )
            return

        self.quiz_index = 0
        self.quiz_score = 0

        self.show_next_question()

    def show_next_question(self):

        if self.quiz_index >= len(
            self.current_user["quiz_questions"]
        ):

            self.show_message(
                "Quiz Finished",
                f"Score: {self.quiz_score}/"
                f"{len(self.current_user['quiz_questions'])}"
            )

            self.show_quiz()

            return

        item = self.current_user[
            "quiz_questions"
        ][self.quiz_index]

        self.clear_screen()

        self.add_title("🧠 QUIZ")

        self.root_layout.add_widget(
            Label(
                text=item["question"],
                size_hint_y=None,
                height=100
            )
        )

        answer = TextInput(
            hint_text="Your answer",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.root_layout.add_widget(answer)

        self.add_button(
            "SUBMIT ANSWER",
            lambda x: self.submit_quiz_answer(
                answer.text
            )
        )

    def submit_quiz_answer(self, answer):

        item = self.current_user[
            "quiz_questions"
        ][self.quiz_index]

        if answer.strip().lower() == item[
            "answer"
        ].strip().lower():

            self.quiz_score += 1

        self.quiz_index += 1

        self.show_next_question()

    # ==========================================
    # STUDY TOOLS
    # ==========================================

    def show_study_tools(self, instance=None):

        self.clear_screen()

        self.add_title("⏱ STUDY TOOLS")

        self.add_button(
            "⏱ STUDY TIMER",
            self.show_timer
        )

        self.add_button(
            "🧮 CALCULATOR",
            self.show_calculator
        )

        self.add_button(
            "💬 MOTIVATIONAL QUOTE",
            self.show_quote
        )

        self.add_button(
            "BACK",
            self.show_dashboard
        )

    # ==========================================
    # TIMER
    # ==========================================

    def show_timer(self, instance=None):

        self.clear_screen()

        self.add_title("⏱ STUDY TIMER")

        self.timer_input = TextInput(
            hint_text="Minutes",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=50
        )

        self.root_layout.add_widget(
            self.timer_input
        )

        self.timer_label = Label(
            text="00:00",
            font_size=35,
            size_hint_y=None,
            height=70
        )

        self.root_layout.add_widget(
            self.timer_label
        )

        self.add_button(
            "START TIMER",
            self.start_timer
        )

        self.add_button(
            "BACK",
            self.show_study_tools
        )

    def start_timer(self, instance):

        try:
            minutes = int(
                self.timer_input.text
            )

            if minutes <= 0:
                raise ValueError

        except ValueError:

            self.show_message(
                "Error",
                "Enter a valid number of minutes."
            )
            return

        self.timer_seconds = minutes * 60

        Clock.schedule_interval(
            self.update_timer,
            1
        )

    def update_timer(self, dt):

        if self.timer_seconds <= 0:

            self.timer_label.text = "00:00"

            return False

        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60

        self.timer_label.text = (
            f"{minutes:02d}:{seconds:02d}"
        )

        self.timer_seconds -= 1

        return True

    # ==========================================
    # CALCULATOR
    # ==========================================

    def show_calculator(self, instance=None):

        self.clear_screen()

        self.add_title("🧮 CALCULATOR")

        self.num1 = TextInput(
            hint_text="First number",
            multiline=False
        )

        self.operation = TextInput(
            hint_text="+  -  *  /",
            multiline=False
        )

        self.num2 = TextInput(
            hint_text="Second number",
            multiline=False
        )

        self.root_layout.add_widget(self.num1)
        self.root_layout.add_widget(self.operation)
        self.root_layout.add_widget(self.num2)

        self.add_button(
            "CALCULATE",
            self.calculate
        )

        self.add_button(
            "BACK",
            self.show_study_tools
        )

    def calculate(self, instance):

        try:

            a = float(self.num1.text)
            b = float(self.num2.text)

            op = self.operation.text.strip()

            if op == "+":
                result = a + b

            elif op == "-":
                result = a - b

            elif op == "*":
                result = a * b

            elif op == "/":

                if b == 0:
                    raise ZeroDivisionError

                result = a / b

            else:
                raise ValueError

            self.show_message(
                "Calculator",
                f"Result: {result}"
            )

        except ZeroDivisionError:

            self.show_message(
                "Error",
                "Cannot divide by zero."
            )

        except ValueError:

            self.show_message(
                "Error",
                "Invalid calculation."
            )

    # ==========================================
    # MOTIVATIONAL QUOTE
    # ==========================================

    def show_quote(self, instance=None):

        quotes = [
            "Small progress is still progress.",
            "Consistency beats talent.",
            "Dream big, code harder!",
            "Your future is built by what you do today.",
            "Keep learning. Keep building. Keep improving.",
            "One step at a time."
        ]

        import random

        self.show_message(
            "💬 Motivation",
            random.choice(quotes)
        )

    # ==========================================
    # PROFILE
    # ==========================================

    def show_profile(self, instance=None):

        self.clear_screen()

        self.add_title("👤 PROFILE")

        user = self.current_user

        self.root_layout.add_widget(
            Label(
                text=f"Name: {user['name']}",
                size_hint_y=None,
                height=45
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"Username: {user['username']}",
                size_hint_y=None,
                height=45
            )
        )

        self.root_layout.add_widget(
            Label(
                text=f"Email: {user['email']}",
                size_hint_y=None,
                height=45
            )
        )

        self.add_button(
            "EDIT DISPLAY NAME",
            self.edit_name_popup
        )

        self.add_button(
            "CHANGE PASSWORD",
            self.change_password_popup
        )

        self.add_button(
            "BACK",
            self.show_dashboard
        )

    def edit_name_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        field = TextInput(
            hint_text="New display name",
            multiline=False
        )

        save = Button(
            text="SAVE",
            size_hint_y=None,
            height=50
        )

        content.add_widget(field)
        content.add_widget(save)

        popup = Popup(
            title="Edit Display Name",
            content=content,
            size_hint=(0.85, 0.4)
        )

        def save_name(instance):

            name = field.text.strip()

            if not name:
                return

            self.current_user["name"] = name

            studyverse_logic.save_data()

            popup.dismiss()

            self.show_profile()

        save.bind(on_press=save_name)

        popup.open()

    def change_password_popup(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        old = TextInput(
            hint_text="Old password",
            password=True,
            multiline=False
        )

        new = TextInput(
            hint_text="New password",
            password=True,
            multiline=False
        )

        confirm = TextInput(
            hint_text="Confirm password",
            password=True,
            multiline=False
        )

        save = Button(
            text="CHANGE PASSWORD",
            size_hint_y=None,
            height=50
        )

        content.add_widget(old)
        content.add_widget(new)
        content.add_widget(confirm)
        content.add_widget(save)

        popup = Popup(
            title="Change Password",
            content=content,
            size_hint=(0.9, 0.65)
        )

        def change(instance):

            if old.text != self.current_user["password"]:
                self.show_message(
                    "Error",
                    "Old password is incorrect."
                )
                return

            if len(new.text) < 8:
                self.show_message(
                    "Error",
                    "Password must be at least 8 characters."
                )
                return

            if new.text != confirm.text:
                self.show_message(
                    "Error",
                    "Passwords do not match."
                )
                return

            self.current_user["password"] = new.text

            studyverse_logic.save_data()

            popup.dismiss()

            self.show_message(
                "Success",
                "Password changed successfully."
            )

        save.bind(on_press=change)

        popup.open()

    # ==========================================
    # DASHBOARD SUMMARY
    # ==========================================

    def show_summary(self, instance=None):

        self.clear_screen()

        self.add_title(
            "📋 DASHBOARD SUMMARY"
        )

        user = self.current_user

        homework_total = len(
            user["homework"]
        )

        homework_done = sum(
            1
            for item in user["homework"]
            if item["status"] == "Done"
        )

        present = user["attendance"]["present"]
        absent = user["attendance"]["absent"]

        attendance_total = present + absent

        attendance_rate = (
            present / attendance_total * 100
            if attendance_total > 0
            else 0
        )

        summary = [
            f"Name: {user['name']}",
            f"Homework: {homework_total}",
            f"Homework Done: {homework_done}",
            f"Study Plans: {len(user['study_plans'])}",
            f"To-Do Tasks: {len(user['todo'])}",
            f"Upcoming Exams: {len(user['exams'])}",
            f"Notes: {len(user['notes'])}",
            f"Quiz Questions: {len(user['quiz_questions'])}",
            f"Attendance: {attendance_rate:.1f}%",
            f"Study Streak: {user['streak']} days"
        ]

        for item in summary:

            self.root_layout.add_widget(
                Label(
                    text=item,
                    size_hint_y=None,
                    height=45
                )
            )

        self.add_button(
            "BACK",
            self.show_dashboard
        )

    # ==========================================
    # LOGOUT
    # ==========================================

    def logout(self, instance=None):

        self.current_user = None

        self.show_welcome()


if __name__ == "__main__":
    StudyVerseApp().run()