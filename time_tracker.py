import tkinter as ttk
from tkinter import Tk, ttk

# Initializes root window
root = Tk()

# Set root window title and dimensions + root window resizing functionality
root.title("Time Tracker")
root.geometry('1920x1080')     # TODO: Add differing window dimensions based on native monitor resolution?
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
tree.column("URL", minwidth=100, width=420)     # TODO: Add max-width for formatting purposes
tree.column("Time Logged", minwidth=100, width=420)
tree.grid(row=0, column=0, columnspan=3, sticky='nsew')  # Spans treeview across top 3 columns and top row.

# TODO: Add horizontal resizing functionality -----DONE------

root.mainloop()
