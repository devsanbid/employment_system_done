import subprocess
import os
import sys

def run_login():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    login_path = os.path.join(current_dir, "a_login.py")
    
    if not os.path.exists(login_path):
        print("Error: a_login.py not found in the current directory.")
        sys.exit(1)
    
    subprocess.run([sys.executable, login_path])

if __name__ == "__main__":
    run_login()
