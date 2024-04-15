import datetime
import tkinter
from tkinter import ttk
import process_tracker
import psutil
import win32gui
import win32process
import time


elapsed_time = 0
start_time = time.time()
process_images = {}


def tracker():

    # TODO: maybe can accomplish this without global variables?
    global elapsed_time
    global start_time
    global process_images

    # Get current process info and put it into a tuple
    try:
        current_process_id = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        current_process_name = psutil.Process(current_process_id[-1]).name()
        current_process_info = current_process_id, current_process_name
        current_process_path = process_tracker.get_process_path(current_process_name)  # TODO: add logic that only runs this code when process_name has changed?
        current_process_icon = process_tracker.get_icon(current_process_path)
    except psutil.NoSuchProcess or ValueError:
        root.after(250, tracker)

    if current_process_icon is not None:
        # Store process icons in a dictionary to efficiently manage image references
        # and prevent potential garbage collection issues.
        process_images[current_process_name] = current_process_icon

    # Updates information if the foreground process has not changed
    if current_process_info == process_tracker.previous_process_info:
        elapsed_time = time.time() - start_time
        time_obj = datetime.timedelta(seconds=elapsed_time)
        process_tracker.update_treeview(tree, current_process_name, time_obj, elapsed_time, process_images[current_process_name])
        start_time = time.time()

    # Handles process changes and starts timer when a change is detected
    if current_process_info != process_tracker.previous_process_info:
        time_obj = datetime.timedelta(seconds=elapsed_time)
        process_tracker.handle_process_change(current_process_info)
        process_tracker.update_treeview(tree, current_process_name, time_obj, elapsed_time, process_images[current_process_name])
        start_time = time.time()

    root.after(250, tracker)


# Initializes root window
root = tkinter.Tk()

# Set root window title and dimensions + root window resizing functionality
root.title("Time Tracker")
root.geometry('1920x1080')  # TODO: Add differing window dimensions based on native monitor resolution?
root.resizable(True, True)

# Configuring columns of root window in order to place treeview
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Configure row of root window in order to add resizing functionality
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Tree view for sorting and displaying process data
columns = ("process_name", "url", "time_logged", "time_val")  # TODO: Add extra columns?
tree = ttk.Treeview(root, columns=columns, displaycolumns=("url", "time_logged"), height=5)

# Adjusting attributes of treeview
tree.heading("#0", text="Process")  # Sets heading text for each column
tree.heading("process_name", text="Process Name")
tree.heading("url", text="URL")
tree.heading("time_logged", text="Time Logged")
tree.heading("time_val", text="Time Value")

tree.column("process_name", width=0)  # Adjusts sizes of columns and treeview
tree.column("url", minwidth=100, width=420)  # TODO: Add max-width for formatting purposes
tree.column("time_logged", minwidth=100, width=420)
tree.column("time_val", width=0)

tree.grid(row=0, column=0, columnspan=3, sticky='nsew')  # Spans treeview across top 3 columns and top row.

# TODO: Add scroll bar for treeview navigation
# TODO: Allow for sorting of treeview columns (sort by most time spent, alphabetical order, etc.)

# Run process tracker and the main loop
tracker()  # TODO: come back to when done separating logic from GUI
root.mainloop()

tree.focus()
