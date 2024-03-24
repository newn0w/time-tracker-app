import psutil
import win32gui
import win32process
import time

# TODO: Add function documentation for code readability
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


def update_treeview(tree, process_name, elapsed_time):
    """
    Updates an existing item in the Treeview with the newly elapsed time, or inserts a new item
    if it doesn't exist yet within the Treeview

    :param tree: The treeview to insert into or modify
    :param process_name: The name of the process to insert
    :param elapsed_time: The total time spent on the process
    """

    global previous_process_info

    # Stores output from checking if current process is in the tree
    search_output = search(tree, process_name)

    if search_output:
        item_elapsed_time = float(tree.item(search_output, "values")[2])  # Converts time value to float for addition

        tree.set(search_output, column=2, value=elapsed_time + item_elapsed_time)
    else:
        tree.insert("", 0, values=(process_name, "TO ADD", elapsed_time))


def search(tree, item_name):
    """
    Searches a treeview widget for an item by comparing an item name to children within the tree.
    If the item name matches the name for a child, return that child's ID. If no matching child is found, return None.

    :param tree: The treeview to search
    :param item_name: The name of the item to compare to children of the tree
    :return: The item ID of the item whose name matches item_name
    """

    children = tree.get_children()

    # Compares names of all values in tree to the searched process name
    for child in children:
        values = tree.item(child, 'values')
        if values[0] == item_name:
            return child

    return None
