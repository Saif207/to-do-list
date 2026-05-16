import datetime
import pyfiglet
import ast
import tkinter as tk
from tkinter import messagebox
import threading
import time

root = tk.Tk()
root.withdraw()


file_name = "tasks.txt"

def save_tasks(input_value,filename):
    with open(filename, 'w') as f:
        f.write(input_value)

def load_tasks(filename):
    with open(filename, 'r') as f:
        return f.read()

try:
    tasks = ast.literal_eval(load_tasks(file_name))
    print("Tasks loaded successfully!", tasks)
except :
    print('creating new file...')
    tasks = []


def add_task():
    while True:

        try:
            task_name = input('Enter the task name: ')
            task_description = input('Enter the task description: ')
            try:
                task_date = input('Enter the task date (YYYY-MM-DD): ')
                task_date = datetime.datetime.strptime(task_date, '%Y-%m-%d').date()

                task_time = input('Enter the task time (HH:MM): ')
                task_time = datetime.datetime.strptime(task_time, '%H:%M').time()

            except ValueError:
                print('Invalid date format. Please enter the date in the format YYYY-MM-DD.')
                continue
            if task_date < datetime.date.today():
                print('The date you entered is in the past. please enter a valid date.')
                continue


            
            if task_name != None and task_description != None and task_date != None and task_time != None:
                tasks.append({
                    'name': task_name,
                    'description': task_description,
                    'date': str(task_date.strftime("%Y-%m-%d")),
                    'time': str(task_time.strftime("%H:%M"))
                })
                save_tasks(str(tasks),file_name)
                
                print(f'Task "{task_name}" added successfully!\n you will be reminded on {task_date} at {task_time} you set! ')
                break
            else:
                print('All fields are required. Redo it again.')
        except ValueError:
            print('Invalid input. Please try again.')


def show_tasks(tasks):
    print('Here are your tasks:')
    for i ,task in enumerate(tasks):
        print(f'Task Number {i+1} : \nTask: {task["name"]}\nDescription: {task["description"]}\nDate: {task["date"]}\nTime: {task["time"]}')

    print("1. Edit Task \n2. Delete Task \n3. Back to main menu")
    try:
        task_choice = str(input("> "))
    except:
        print('Invalid input try again...')
    
    if task_choice == '1':
            print('Edit Task\n')
            for i ,task in enumerate(tasks):
                print(f'Task Number {i+1} : \nTask: {task["name"]}\nDescription: {task["description"]}\nDate: {task["date"]}\nTime: {task["time"]}')
            print('Enter the task number you want to edit')
            edit_choice = int(input("> "))

            if edit_choice > len(tasks) or edit_choice < 1:
                print('Invalid task number. Please try again.')
            else:
                chosen_task = tasks[edit_choice - 1]
                print(chosen_task)
                print('What do you want to edit? \n1. Task Name \n2. Task Description \n3. Task Date \n4. Task Time')
                edit_field_choice = str(input("> "))
                if edit_field_choice == '1':
                    new_task_name = input('Enter the new task name: ')
                    chosen_task['name'] = new_task_name
                    save_tasks(str(tasks),file_name)
                    print('Task name updated successfully!')

                elif edit_field_choice == '2':
                    new_task_description = input('Enter the new task description: ')
                    chosen_task['description'] = new_task_description
                    save_tasks(str(tasks),file_name)
                    print('Task description updated successfully!')

                elif edit_field_choice == '3':
                    try:
                        new_task_date = input('Enter the new task date (YYYY-MM-DD): ')
                        new_task_date = datetime.datetime.strptime(new_task_date, '%Y-%m-%d').date()
                        if new_task_date < datetime.date.today():
                            print('The date you entered is in the past. please enter a valid date.')
                        else:
                            chosen_task['date'] = str(new_task_date)
                            save_tasks(str(tasks),file_name)
                            print('Task date updated successfully!')
                    except ValueError:
                        print('Invalid date format. Please enter the date in the format YYYY-MM-DD.')
                elif edit_field_choice == '4':
                    try:
                        new_task_time = input("Enter the new task time (HH:MM): ")
                        new_task_time = datetime.datetime.strptime(new_task_time, '%H:%M').time()
                        chosen_task['time'] = str(new_task_time.strftime("%H:%M"))
                        save_tasks(str(tasks),file_name)
                        print(f'Task time has been updated from {chosen_task["time"]}, to {new_task_time} successfully!')
                    except ValueError:
                        print('Invalid time format. Please enter the time in the format HH:MM.')
                else:
                    print('Invalid choice. Please try again.')
            

    elif task_choice == '2':
        print('Delete Task')
        for i ,task in enumerate(tasks):
            print(f'Task Number {i+1} : \nTask: {task["name"]}\nDescription: {task["description"]}\nDate: {task["date"]}\n')
        print('Enter the task number you want to delete')
        delete_choice = int(input("> "))

        if delete_choice > len(tasks) or delete_choice < 1:
            print('Invalid task number. Please try again.')
        
        else:
            deleted_task = tasks.pop(delete_choice -1)
            save_tasks(str(tasks),file_name)
            print(f'Task "{deleted_task["name"]}" deleted successfully!')


    elif task_choice == '3':
        return

def reminder():
    while True:
        now = datetime.datetime.now()
        for task in tasks:
            if task['date'] == now.strftime("%Y-%m-%d") and task['time'] == now.strftime("%H:%M"):
                root.after(0, lambda t=task: messagebox.showinfo(
                    "Task Reminder",
                    f"Task: {t['name']}\nDescription: {t['description']}\nDate: {t['date']}\nTime: {t['time']}"
                ))
        time.sleep(60)

def main():
    print(pyfiglet.figlet_format("To-Do List", font="slant"))
    print("   Welcome to To-Do List!\n")
    threading.Thread(target=reminder, daemon=True).start()
    while True:
        print(" Please select an option: \n 1. Add a task \n 2. Show tasks \n 3. Exit")
        choice = str(input("> "))
        if choice == '1':
            add_task()
        elif choice == '2':
            show_tasks(tasks)
        elif choice == '3':
            print("Goodbye!")
            root.quit()
            break
        else:
            print("Invalid choice. Try again...")

threading.Thread(target=main,daemon=True).start()
root.mainloop()

