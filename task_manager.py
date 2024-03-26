# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#==== Defined Functions====
def clear_screen():
    os.system("clear || cls")


def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username, check to see if it already exists,
    # - and prompt again.
    while True:
        new_username = input("New Username: ").lower()
        with open('user.txt', 'r') as in_file:
            
            # - Iterates over each line of user.txt, splitting the line at 
            # - each ';', and keeping only the username at index [0].
            for line in in_file:
                current_usernames = line.strip().split(';')
                current_usernames = current_usernames[0]

            if new_username in current_usernames:
                print("Username already exists. Please try again:")
                continue
            
            else:
                break

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
    '''Allow a user to add a new task to task.txt file
         Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    while True:
        task_username = input("Name of person assigned to task: ").lower()
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)

        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        break


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    global task_count
    task_count = []
    
    for i, t in enumerate(task_list, 1):
        if t['username'] == curr_user:
            disp_str = f"Task Number: {i}\n"
            disp_str += f"Task: \t\t {t['title']}\n" 
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t \
            {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t \
            {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            task_count.append(i)


def mark_task(task_selection):
    # Marks a selected task as complete, and ammends tasks.txt appropriately.

    # Opens tasks.txt in read mode, splits file and assigns value to 
    # dictionary tasks.
    with open("tasks.txt", 'r') as task_file:
        tasks = []
        for line in task_file:
            split_file_line = line.strip().split(';')
            task_dict = {"username": split_file_line[0],
                         "title": split_file_line[1],
                         "description": split_file_line[2],
                         "due_date": split_file_line[3],
                         "assigned_date": split_file_line[4],
                         "completed": split_file_line[5]
                         }
            tasks.append(task_dict)

    # Changes value of "completed" key to "Yes", and the "completed" key value
    # task_selection at index task_selection, in task_list to True. 
    task_edit = tasks[task_selection]
    task_edit["completed"] = "Yes"
    task_list[task_selection]["completed"] = True

    # Opens tasks.txt to ammend the file. 
    with open("tasks.txt", 'w') as task_file:
        for task in tasks:
            task_file.write(f"{task['username']};{task['title']};"
                    f"{task['description']};{task['due_date']};"
                    f"{task['assigned_date']};{task['completed']}\n")
            
    print("Edit has been saved, and task is now marked as complete.")
    

def edit_task(task_selection):
    # Allows user to edit task's assigned user or the task due date. 
    # Task can only be edited if task is not complete.

    # Read tasks.txt, and split lines and values, then
    # append to tasks[].
    with open("tasks.txt", 'r') as task_file:
        tasks = []
        for line in task_file:
            split_file_line = line.strip().split(';')
            task_dict = {"username": split_file_line[0],
                        "title": split_file_line[1],
                        "description": split_file_line[2],
                        "due_date": split_file_line[3],
                        "assigned_date": split_file_line[4],
                        "completed": split_file_line[5]
                        }
            tasks.append(task_dict)

    # Check to see if task is already complete.
    if tasks[task_selection]["completed"] == "Yes":
        print("This task has already been completed and cannot be ammended.")
        return

    while True:
        user_choice = input("Please select an option:\nr - Reassign task\n"
                            "m - Modify due date\n").lower()
        
        if user_choice == 'r':
            while True:
                new_username = input("Please enter the username to whom you"
                                     " wish to reassign the task:\n")
                if new_username in username_password.keys():
                   

                    # Ammends username in list
                    task_edit = tasks[task_selection]
                    task_edit["username"] = new_username
                    task_list[task_selection]["username"] = new_username

                    # Writes ammendment back to tasks.txt
                    with open("tasks.txt", 'w') as task_file:
                        for task in tasks:
                            task_file.write(f"{task['username']};"
                                            f"{task['title']};"
                                            f"{task['description']};"
                                            f"{task['due_date']};"
                                            f"{task['assigned_date']};"
                                            f"{task['completed']}\n")
                            
                    print("Task has been successfully reassigned.")
                    break
            break

        elif user_choice == 'm':
            # Read tasks.txt, and split lines and values, then
            # append to tasks[].
            while True:
                try:
                    task_due_date = input("Please enter new due-date (YYYY-MM-DD):\n")
                    due_date_time = datetime.strptime(task_due_date,\
                                    DATETIME_STRING_FORMAT).date()
                    break

                except ValueError:
                    print("\nInvalid datetime format. "
                        "Please use the format specified")

            # Ammends username in list
            task_edit = tasks[task_selection]
            task_edit["due_date"] = due_date_time
            task_list[task_selection]["due_date"] = due_date_time

            # Writes ammendment back to tasks.txt
            with open("tasks.txt", 'w') as task_file:
                for task in tasks:
                    task_file.write(f"{task['username']};"
                                    f"{task['title']};"
                                    f"{task['description']};"
                                    f"{task['due_date']};"
                                    f"{task['assigned_date']};"
                                    f"{task['completed']}\n")
                    
            print("Due date has been successfully ammended.")
            break
                
        else:
            print("Error- please enter either 'r' or 'm' for the option" 
                  "required")


def generate_task_overview():
    """
    Generate a task overview, containing number of completed tasks,
    incomplete tasks, and overdue tasks. Percentages for the final two 
    in relation to total tasks wis calculated, and all of this is written to
    task_overview.txt.
    """
    complete_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0

    for task in task_list:
        completed_tasks = task.get("completed", True)
        if completed_tasks:
            complete_tasks += 1
        elif not completed_tasks:
            incomplete_tasks += 1
            if "due_date" in task:
                due_date = task["due_date"]
                if due_date < datetime.today():
                    overdue_tasks += 1
    
    total_tasks = len(task_list)

    # Calculate percentages for complete, incomplete and overdue tasks.
    complete_percent = (complete_tasks / total_tasks) * 100
    incomplete_percent = (incomplete_tasks / total_tasks) * 100
    overdue_percent = (overdue_tasks / total_tasks) * 100

    # Writes information to a task_overview.txt
    with open("task_overview.txt", 'w') as overview_file:
        overview_file.write("***** Task Overview Report *****\n\n")
        overview_file.write(f"Total tasks: \t\t\t\t{total_tasks}\n")
        overview_file.write('*' * 40)
        overview_file.write("\nCompleted tasks: "
                            f"\t\t\t{complete_tasks}\n")
        overview_file.write("Incomplete tasks: "
                            f"\t\t\t{incomplete_tasks}\n")
        overview_file.write("Overdue tasks: "
                            f"\t\t\t\t{overdue_tasks}\n\n")
        overview_file.write('*' * 40)               
        overview_file.write("\nPercentage completed: "
                            f"\t\t{complete_percent}\n")
        overview_file.write("Percentage incomplete: "
                            f"\t\t{incomplete_percent}\n")
        overview_file.write("Percentage overdue: "
                            f"\t\t{overdue_percent}\n")


def generate_user_overview(task_list, username_password):
    """
    Generate a user overview report, which details total number of registered 
    users and tasks. It also includes total number of tasks assigned to each
    user, and the percentage of total tasks assigned to that user. It then 
    calculates the percentage of tasks assigned to user which have been 
    completed, are incomplete, and are overdue.
    """
    total_users = len(username_password)
    total_tasks = len(task_list)

    with open("user_overview.txt", 'w') as user_overview:
        user_overview.write("***** User Overview Report *****\n\n")
        user_overview.write("Total registered users: "
                            f"\t{total_users}\n")
        user_overview.write("Total number of tasks: \t\t"
                            f"{total_tasks}\n\n")
            
        for username in sorted(username_password):      # Sorted for alphabetical
            user_task_list = [task for task in task_list if task['username'] \
                            == username]
            user_total_tasks = len(user_task_list)
            complete_tasks = 0
            incomplete_tasks = 0
            overdue_tasks = 0

            for task in user_task_list:
                completed_tasks = task.get("completed", True)
                if completed_tasks:
                    complete_tasks += 1
                elif not completed_tasks:
                    incomplete_tasks += 1
                    if "due_date" in task:
                        due_date = task["due_date"]
                        if due_date < datetime.today():
                            overdue_tasks += 1

            user_assigned_percent = (user_total_tasks / total_tasks) * 100
            user_complete_percent = (complete_tasks / user_total_tasks) * 100
            user_incomplete_percent = (incomplete_tasks / user_total_tasks) * 100
            user_overdue_percent = (overdue_tasks / user_total_tasks) * 100
            
            user_overview.write('*' * 40)
            user_overview.write(f"\nUsername: {username}\n")
            user_overview.write(f"Total tasks assigned: \t\t{user_total_tasks}\n")
            user_overview.write("Percentage of total: \t\t"
                                f"{user_assigned_percent}\n")
            user_overview.write("Percentage of completed: \t"
                                f"{user_complete_percent}\n")
            user_overview.write("Percentage of incomplete: \t"
                                f"{user_incomplete_percent}\n")
            user_overview.write("Percentage of overdue: \t\t"
                                f"{user_overdue_percent}\n\n")
        

########### Main Code Block ###########

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:\n
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()
    clear_screen()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()
            
    elif menu == 'vm':
        
        while True:
            view_mine()
            
            user_choice = input("Please enter the number of the task you"
                " wish to edit, or enter '-1' to return to main menu: \n")
            
            # Validate user_choice is a numeric entry       
            if user_choice.isnumeric():
                task_selection = int(user_choice)

                # Calculate index value from user_choice
                if task_selection in task_count:
                    task_selection = int(user_choice) - 1
                    break
                
                # Error handling.
                else:
                    print("Task number does not exist. Please enter a valid"
                          " task entry:\n")
                    
            elif user_choice == "-1":
                break
            
            # Error handling.
            else:
                print("Error. Please enter a valid menu number:\n")

        # Return to main menu.
        if user_choice == "-1":
            continue
        
        while True:
            # Menu for user to decide whether to mark or edit task
            user_choice = input("Would you like to edit or mark the selected "
                                "task as complete?\n Please type 'edit' or "
                                "'mark':\n")
            
            if user_choice.lower() == "mark":
                mark_task(task_selection)
                break

            elif user_choice.lower() == 'edit':
                edit_task(task_selection)
                break

            else:
                print("Error. Please enter either 'edit' or mark':\n")

    elif menu == 'gr' and curr_user == 'admin':
        generate_task_overview()
        generate_user_overview(task_list, username_password)

        print("Task overview and user overview reports generated "
              "successfully")
                
    elif menu == 'ds' and curr_user == 'admin': 
        """
        If the user is an admin they can display statistics from 
        user_overview.txt and task_overview.txt. If they do not exist yet,
        program generates those reports.
        """
        if not os.path.exists("task_overview.txt") or not \
        os.path.exists("user_overview.txt"):
            generate_task_overview()
            generate_user_overview(task_list, username_password)

            print("Task overview and user overview reports generated "
              "successfully")
        
        with open("task_overview.txt", 'r') as task_overview:
            print(task_overview.read())

        with open("user_overview.txt", 'r') as user_overview:
            print(user_overview.read())

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")