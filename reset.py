from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess

def reset_password():
    current_password = Currentpassword_Entry.get()
    new_password = Newpassword_Entry.get()
    retype_new_password = Retypenewpassword_Entry.get()
    
    if not all([current_password, new_password, retype_new_password]):
        messagebox.showerror("Error", "All fields are required")
        return
    
    if new_password != retype_new_password:
        messagebox.showerror("Error", "New passwords do not match")
        return
    
    if len(new_password) < 8:
        messagebox.showerror("Error", "New password must be at least 8 characters long")
        return
    
    conn = sqlite3.connect('employeemanagement.db')
    cursor = conn.cursor()
    
    # Verify current password
    cursor.execute("SELECT * FROM users WHERE password = ?", (current_password,))
    user = cursor.fetchone()
    
    if user:
        # Update password
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user[0]))
        conn.commit()
        messagebox.showinfo("Success", "Password has been reset successfully")
        root.destroy()  # Close the reset password window
        subprocess.Popen(["python", "a_login.py"])  # Open the login page
    else:
        messagebox.showerror("Error", "Current password is incorrect")
    
    conn.close()

def exit_window():
    root.destroy()
    subprocess.Popen(["python", "a_login.py"])  # Open the login page

root = Tk()
root.title("Employee Management System - Reset Password")
root.config(bg="#1E2E56")
root.geometry("1200x700")  # Set a specific size for the window

EMs = Label(text="Employee Management System", font=("Arial", 24, "bold"), bg="#1E2E56", fg="white")
EMs.place(x=400, y=13)

Resetpassword = Label(text="Reset Password", font=("Arial", 22, "bold"), bg="#1E2E56", fg="white")
Resetpassword.place(x=500, y=85)

Currentpassword = Label(text="Current password", bg="#1E2E56", fg="white", font=("Arial", 20))
Currentpassword.place(x=150, y=165)
Currentpassword_Entry = Entry(root, font=("Arial", 20), show="*")
Currentpassword_Entry.place(x=450, y=170)

Newpassword = Label(text="New password", bg="#1E2E56", fg="white", font=("Arial", 20))
Newpassword.place(x=150, y=280)
Newpassword_Entry = Entry(root, font=("Arial", 20), show="*")
Newpassword_Entry.place(x=450, y=280)

Retypenewpassword = Label(text="Retype new password", bg="#1E2E56", fg="white", font=("Arial", 20))
Retypenewpassword.place(x=120, y=400)
Retypenewpassword_Entry = Entry(root, font=("Arial", 20), show="*")
Retypenewpassword_Entry.place(x=450, y=400)

Confirm = Button(text="Confirm", font=("Arial", 20), command=reset_password, bg="#4CAF50", fg="white")
Confirm.place(x=450, y=500)

Exit = Button(text="Exit", font=("Arial", 20), command=exit_window, bg="#f44336", fg="white")
Exit.place(x=650, y=500)

mainloop()
