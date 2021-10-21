import os
import sqlite3
import tkinter.filedialog
from tkinter import Tk

from CalculateTask import CalculateTask


def prompt_for_database_path():
    tk = Tk()
    tk.withdraw()
    return tkinter.filedialog.SaveAs(tk).show().replace('.db', '') + ".db"


def create_database(path):
    table_name = "prime_numbers"
    column_name = "number"
    connection = sqlite3.connect(path)
    connection.executescript(
        f"""DROP TABLE IF EXISTS {table_name}; 
        CREATE TABLE {table_name} ({column_name} INTEGER NOT NULL UNIQUE); 
        PRAGMA auto_vacuum = '2'; 
        VACUUM; 
        PRAGMA journal_mode = 'WAL';""")
    return column_name, connection, table_name


def prompt_for_range():
    start_number = prompt_for_number(is_start_number=True)
    end_number = prompt_for_number(is_start_number=False)
    if len(range(start_number, end_number)) == 0:
        print('Invalid range. Please retry.\n')
        return prompt_for_range()
    else:
        return start_number, end_number


def prompt_for_number(is_start_number=True, is_invalid=False):
    prompt_text = f"Type the number from which to {'start' if is_start_number else 'stop'} calculating: "
    try:
        prompt_response = input(f"Invalid entry. {prompt_text}" if is_invalid else prompt_text)
        value = int(prompt_response)
        if value <= 0:
            raise ValueError
        else:
            return value
    except ValueError:
        return prompt_for_number(is_start_number, True)


def create_tasks(start, end):
    tasks = []
    core_count = os.cpu_count()
    amount_to_take_per_task = int(end / core_count)
    cores_counted = 0

    while cores_counted != core_count:
        end = start + amount_to_take_per_task
        if end > end:
            end = end

        task = CalculateTask(cores_counted + 1, start, end)
        tasks.append(task)

        start = end + 1
        cores_counted += 1

    return tasks


def execute_tasks(column_name, connection, table_name, tasks):
    for task in tasks:
        task.start()
    print('Calculating...')
    while True:
        all_tasks_done = True
        for task in tasks:
            if task.running:
                all_tasks_done = False
                break

        for task in tasks:
            container = task.calculated_numbers
            while not container.empty():
                connection.execute(f'INSERT INTO {table_name} ({column_name}) VALUES ({str(container.get())})')

        if all_tasks_done:
            print("Almost done!")
            connection.commit()
            connection.close()
            print("Finished!")
            break


def main():
    path = prompt_for_database_path()
    start_number, end_number = prompt_for_range()
    column_name, connection, table_name = create_database(path)
    tasks = create_tasks(start_number, end_number)
    execute_tasks(column_name, connection, table_name, tasks)


if __name__ == '__main__':
    main()
