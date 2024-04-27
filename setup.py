import os
import subprocess

# Install dependencies
subprocess.run(["pip", "install", "-r", "requirements.txt"])

# Build the project
subprocess.run(["pyinstaller", "time_tracker.py", "--onefile"])

# Create an executable file
exe_file = "time_tracker.exe"
if os.path.exists(exe_file):
    os.remove(exe_file)
os.rename("dist/time_tracker.exe", exe_file)

print("Build complete. Please run the executable file to run the program.")
