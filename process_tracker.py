import os
import wmi
import time
import tkinter
import psutil
import win32gui
import win32process
import icoextract  # TODO: maybe remove? use PIL instead?
from PIL import Image, ImageTk

previous_process_info = None
process_data = {}


# Get and store data of the current foreground process
def get_foreground_process_info():
    """
    Retrieves information about the current foreground process.

    :return: A tuple containing (process ID, process name) or None if no foreground process is found.
    """

    try:
        current_process_id = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        current_process_name = psutil.Process(current_process_id[-1]).name()

        return current_process_id, current_process_name

    except (IndexError, psutil.NoSuchProcess):
        return None


# Check if foreground process has changed and adjust accordingly
def handle_process_change(current_process_info):
    """
    Checks for any changes in foreground process and updates internal state accordingly.

    :param current_process_info: A tuple containing (process ID, process name) for the current process.
    :return: A tuple containing (process ID, process name) for the previously logged process.
    """

    global previous_process_info

    # Handle case where no foreground process is found
    if not current_process_info:
        return

    # If foreground process has changed, handle accordingly
    if previous_process_info:
        previous_process_info = current_process_info  # Update for next function call

    # Sets previous_process_info as current_process_info on first iteration of function
    if not previous_process_info:
        previous_process_info = current_process_info

    return previous_process_info


# Track total time spent on a specific process
def track_elapsed_time(start_time):
    """
    Calculates the elapsed time for any specific process.

    :param start_time: The time when the specified process became the foreground process.
    :return: The elapsed time in seconds.
    """

    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time


def get_process_path(process_name):
    """
    Retrieves the path of a given process.

    :param process_name: The name of the process to find the path for.
    :return:
    """

    # Create a WMI object for accessing process information
    c = wmi.WMI()

    # Iterate through processes to find directory of provided process
    for process in c.Win32_process(name=process_name):
        return process.ExecutablePath  # Returns process directory when found

    # If no matches are found, return none
    return None


def get_icon(path):
    """
    Takes the path for a file and extracts the icon of that file.

    :param path: The file path for the file whose icon we wish to extract.
    :return: The icon for the process whose path was given.
    """

    # Attempt to extract icon from path parameter
    try:
        icon_extractor = icoextract.IconExtractor(path)  # Initializes IconExtractor object with path parameter
        file_icon = icon_extractor.get_icon()  # Stores the executable icon as a BytesIO object
        icon_data = Image.open(file_icon)  # Reads the BytesIO object and produces the raw bytes
        resized_icon = icon_data.resize((16, 16))
        process_icon = ImageTk.PhotoImage(resized_icon)

        print("File name gotten!")
        print(f"File icon: {resized_icon}")
        print("Attempting to show image...")
        # icon_data.show()
        print(f"Printing ImageTk variable from get_icon: {process_icon}")
        return process_icon
    except icoextract.NoIconsAvailableError:
        print(icoextract.NoIconsAvailableError)  # TODO: Implement handling of cases w/ no icon


def update_treeview(tree, process_name, elapsed_time, process_icon):
    """process_icon
    Updates an existing item in the Treeview with the newly elapsed time, or inserts a new item
    if it doesn't exist yet within the Treeview.

    :param tree: The treeview to insert into or modify.
    :param process_name: The name of the process to insert.
    :param elapsed_time: The total time spent on the process.
    """

    global previous_process_info

    # Stores output from checking if current process is in the tree
    search_output = tree_search(tree, process_name)

    if search_output:
        item_elapsed_time = float(tree.item(search_output, "values")[2])  # Converts time value to float for addition
        tree.set(search_output, column=2, value=elapsed_time + item_elapsed_time)  # Updates the item in the treeview

        # Set image again after updating time due to GUI redrawing
        tree.item(search_output, image=process_icon)
    else:
        tree.insert("", 0, image=process_icon, text=process_name, value=(process_name, "TO ADD", elapsed_time))



def tree_search(tree, item_name):
    """
    Searches a treeview widget for an item by comparing an item name to children within the tree.
    If the item name matches the name for a child, return that child's ID. If no matching child is found, return None.

    :param tree: The treeview to search.
    :param item_name: The name of the item to compare to children of the tree.
    :return: The item ID of the item whose name matches item_name.
    """

    children = tree.get_children()

    # Compares names of all values in tree to the searched process name
    for child in children:
        values = tree.item(child, 'values')
        print(values)
        if values[0] == item_name:
            print(f"value[0]: {child}")
            return child

    return None
