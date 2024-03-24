from tkinter import Tk, ttk
import process_tracker
import psutil
import win32gui
import win32process
import time


elapsed_time = 0
start_time = time.time()


def tracker():
    print(f"process_tracker func: {process_tracker.get_foreground_process_info()}")

    # TODO: maybe can accomplish this without global variables?
    global elapsed_time
    global start_time

    # Get current process info and put it into a tuple
    current_process_id = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    current_process_name = psutil.Process(current_process_id[-1]).name()
    current_process_info = current_process_id, current_process_name

    # Updates information if the foreground process has not changed
    if current_process_info == process_tracker.previous_process_info:
        elapsed_time = time.time() - start_time
        process_tracker.update_treeview(tree, current_process_name, elapsed_time)
        start_time = time.time()

    # Handles process changes and starts timer when a change is detected
    if current_process_info != process_tracker.previous_process_info:
        process_tracker.handle_process_change(current_process_info)
        process_tracker.update_treeview(tree, current_process_name, elapsed_time)
        start_time = time.time()

    root.after(250, tracker)


# Initializes root window
root = Tk()

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
columns = ("Process", "URL", "Time Logged")  # TODO: Add extra columns?
tree = ttk.Treeview(root, columns=columns, show="headings", height=5)

# Adjusting attributes of treeview
tree.heading("Process", text="Process")  # Sets heading text for each column
tree.heading("URL", text="URL")
tree.heading("Time Logged", text="Time Logged")
tree.column("Process", minwidth=100, width=420)  # Adjusts sizes of columns and treeview
tree.column("URL", minwidth=100, width=420)  # TODO: Add max-width for formatting purposes
tree.column("Time Logged", minwidth=100, width=420)

tree.grid(row=0, column=0, columnspan=3, sticky='nsew')  # Spans treeview across top 3 columns and top row.

# TODO: Add scroll bar for treeview navigation
# TODO: Allow for sorting of treeview columns (sort by most time spent, alphabetical order, etc.)

tracker()  # TODO: come back to when done separating logic from GUI
root.mainloop()

# root.after(1000, track_processes(tree))
tree.focus()
