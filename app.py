import streamlit as st
from supabase import create_client, Client
# from dotenv import load_dotenv
import os
from backed import add_task, get_tasks, update_task, delete_task

supabase_url = "https://knkmsszpwvyamvqqsana.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtua21zc3pwd3Z5YW12cXFzYW5hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYxMjI1NTAsImV4cCI6MjA3MTY5ODU1MH0.hr2Op4urTZNhVG_fL1m8GRBt3HHiXI2ljXDVqWt9jzc"
supabase: Client = create_client(supabase_url, supabase_key)

# --- Auth Functions ---
def sign_up(email, password):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")

# --- Task Dashboard ---
def task_dashboard():
    st.title("📝 Task Manager")
    option = st.selectbox("Choose an action", ["Add Task", "View Tasks", "Update Task Status", "Delete Task"])

    if option == "Add Task":
        title = st.text_input("Task Title")
        description = st.text_area("Description")
        status = st.text_input("Status")
        if st.button("Add"):
            res = add_task(title, description,status)
            st.success("✅ Task added!")

    elif option == "View Tasks":
        tasks = get_tasks()
        st.subheader("📋 Your Tasks")
        for task in tasks:
            st.write(f"**{task['id']} - {task['Title']}**: {task['Status']}")

    elif option == "Update Task Status":
        task_id = st.text_input("Enter Task ID")
        new_status = st.selectbox("Select New Status", ["pending", "in progress", "done"])
        if st.button("Update"):
            res = update_task(task_id, new_status)
            st.success("🔄 Task updated!")

    elif option == "Delete Task":
        task_id = st.text_input("Enter Task ID to delete")
        if st.button("Delete"):
            res = delete_task(task_id)
            st.success("🗑️ Task deleted!")

    if st.button("Logout"):
        sign_out()

# --- Auth UI ---
def auth_screen():
    st.title("🔐 Login / Sign Up")
    option = st.selectbox("Choose an action:", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Sign Up" and st.button("Register"):
        user = sign_up(email, password)
        if user and user.user:
            st.success("Registration successful. Please log in.")

    if option == "Login" and st.button("Login"):
        user = sign_in(email, password)
        if user and user.user:
            st.session_state.user_email = user.user.email
            st.success(f"Welcome back, {email}!")
            st.rerun()

# --- App State Management ---
if "user_email" not in st.session_state:
    st.session_state.user_email = None

if st.session_state.user_email:
    task_dashboard()
else:
    auth_screen()
