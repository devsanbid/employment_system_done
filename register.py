import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import re
import subprocess

def create_database():
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT DEFAULT NULL,
    phone TEXT DEFAULT NULL,
    position TEXT DEFAULT NULL,
    department TEXT DEFAULT NULL,
    address TEXT DEFAULT NULL
)''')
    conn.commit()
    conn.close()

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def toggle_password_visibility():
    global show_password
    show_password = not show_password
    show_char = '' if show_password else '*'
    password_entry.config(show=show_char)
    confirm_password_entry.config(show=show_char)
    show_password_button.config(text='Hide Passwords' if show_password else 'Show Passwords')

def register():
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not all([email, username, password, confirm_password]):
        messagebox.showerror("Error", "All fields are required")
        return

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    if len(password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long")
        return

    try:
        conn = sqlite3.connect('employeemanagement.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                       (email, username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
        root.destroy()  # Close the registration window
        subprocess.Popen(["python", "a_login.py"])  # Open the login page
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email or username already exists")
    finally:
        conn.close()

# Create the database and table
create_database()

# Create the main window
root = tk.Tk()
root.title("Employee Management System - Registration")
root.config(bg="#1E2E56")
root.geometry("400x600")

# Configure styles
style = ttk.Style()
style.theme_use('clam')
style.configure('TEntry', padding=5, relief='flat')
style.configure('TButton', padding=10, relief='flat', background="#4CAF50", foreground="white")
style.map('TButton', background=[('active', '#45a049')])

# Create and place widgets
tk.Label(root, text="Registration", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white").pack(pady=20)

tk.Label(root, text="Email", bg="#1E2E56", fg="white", font=("Arial", 12)).pack()
email_entry = ttk.Entry(root, font=("Arial", 12), width=30)
email_entry.pack(pady=5)

tk.Label(root, text="Username", bg="#1E2E56", fg="white", font=("Arial", 12)).pack()
username_entry = ttk.Entry(root, font=("Arial", 12), width=30)
username_entry.pack(pady=5)

tk.Label(root, text="Password", bg="#1E2E56", fg="white", font=("Arial", 12)).pack()
password_entry = ttk.Entry(root, font=("Arial", 12), show="*", width=30)
password_entry.pack(pady=5)

tk.Label(root, text="Confirm Password", bg="#1E2E56", fg="white", font=("Arial", 12)).pack()
confirm_password_entry = ttk.Entry(root, font=("Arial", 12), show="*", width=30)
confirm_password_entry.pack(pady=5)

show_password = False
show_password_button = ttk.Button(root, text="Show Passwords", command=toggle_password_visibility)
show_password_button.pack(pady=10)

register_button = ttk.Button(root, text="Register", command=register)
register_button.pack(pady=20)

root.mainloop()
