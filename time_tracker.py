import tkinter as ttk
from tkinter import Tk, ttk

# Initializes root window
root = Tk()

# Set root window title and dimensions
root.title("Time Tracker")
root.geometry('1280x700')

# Configuring columns of root window in order to place treeview
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Tree view for sorting and displaying process data
columns = ("Process", "URL", "Time Logged")  # TODO: Add extra columns?
tree = ttk.Treeview(root, columns=columns, show="headings", height=19)

# Adjusting attributes of treeview
tree.heading("Process", text="Process")  # Sets heading text for each column
tree.heading("URL", text="URL")
tree.heading("Time Logged", text="Time Logged")
tree.column("Process", minwidth=0, width=420)  # Adjusts sizes of columns and treeview
tree.column("URL", minwidth=0, width=420)
tree.column("Time Logged", minwidth=0, width=420)
tree.grid(row=2, column=0, columnspan=3, sticky='ew')  # Spans treeview across top 3 columns.

# TODO: Add horizontal resizing functionality

root.mainloop()
