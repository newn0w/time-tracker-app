import tkinter
from tkinter import ttk

import process_tracker
import psutil
import win32gui
import win32process
import time
import datetime


elapsed_time = 0
start_time = time.time()
process_images = {}
selected_process_icon = None


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
        current_process_icon = process_tracker.get_icon(current_process_path, size=(16, 16))
        process_info_icon = process_tracker.get_icon(current_process_path, size=(128, 128))
    except psutil.NoSuchProcess or ValueError:
        root.after(250, tracker)

    if current_process_icon is not None:
        # Store full size and resized process icons in a dictionary to efficiently manage image references
        # and prevent potential garbage collection issues.
        process_images[current_process_name] = (current_process_icon, process_info_icon)

    # Updates information if the foreground process has not changed
    if current_process_info == process_tracker.previous_process_info:
        elapsed_time = time.time() - start_time
        time_obj = datetime.timedelta(seconds=elapsed_time)
        process_tracker.update_treeview(tree, current_process_name, time_obj, elapsed_time, process_images[current_process_name][0])
        start_time = time.time()

    # Handles process changes and starts timer when a change is detected
    if current_process_info != process_tracker.previous_process_info:
        time_obj = datetime.timedelta(seconds=elapsed_time)
        process_tracker.handle_process_change(current_process_info)
        process_tracker.update_treeview(tree, current_process_name, time_obj, elapsed_time, process_images[current_process_name][0])
        start_time = time.time()

    root.after(250, tracker)


def handle_treeview_click(event):
    global selected_process_icon
    current_item = tree.selection()

    try:
        if not current_item:
            pass  # Do nothing if no item is selected

        process_name = tree.item(current_item, "values")[0]

        if process_name:
            selected_process_icon = process_images.get(process_name)[1]

        icon_label.config(image=selected_process_icon)
    except IndexError:
        tree.selection_remove(current_item)
        pass


# Initializes root window
root = tkinter.Tk()

# Set root window title and dimensions + root window resizing functionality
root.title("Time Tracker")
root.geometry('1280x720')  # TODO: Add differing window dimensions based on native monitor resolution?
root.resizable(True, True)

# Create a frame to hold the icon and information labels
info_frame = tkinter.Frame(root, padx=30, pady=30)
info_frame.pack(side='bottom', fill='x')  # Adjust packing order as needed

# Create a label widget below the treeview for displaying the icon
icon_label = tkinter.Label(info_frame, image='', anchor='w')
icon_label.pack(side='left')  # Adjust placement within info_frame

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

tree.config(height=15)

tree.pack(fill='both', expand=True)  # Fills remaining space in root window

tree.bind("<ButtonRelease-1>", handle_treeview_click)  # Handles selection of items in the tree

# TODO: Add scroll bar for treeview navigation
# TODO: Allow for sorting of treeview columns (sort by most time spent, alphabetical order, etc.)

# Run process tracker and the main loop
tracker()  # TODO: come back to when done separating logic from GUI
root.mainloop()

tree.focus()
