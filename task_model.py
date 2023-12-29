import sqlite3 # to use a database for storing tasks
from datetime import datetime # to handle dates and times
from task import Task

class TaskModel:

    def __init__(self) -> None:
        # create a connection to the database file
        self.conn = sqlite3.connect("tasks.db")
        # create a cursor object to execute SQL commands
        cur = self.conn.cursor()
        # create a table named tasks if it does not exist
        cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            NAME TEXT NOT NULL,
            description TEXT ,
            Due_Date TEXT ,
            priority BOOLEAN ,
            status BOOLEAN ,
            List_Name TEXT
            )""")
        # commit the changes to the database
        self.conn.commit()
        self.categories : set[Task] = set()
        self.update_categories()
        

    def add_task(self,Task):
        self.cur = self.conn.cursor()
        self.cur.execute("""INSERT INTO tasks(name ,description , due_date, priority , status ,  list_name)VALUES (?, ?, ?, ?, ? , ?)""",(Task.name,Task.description,Task.due_date,Task.priority,Task.status,Task.list_name))
        Task.id = self.cur.lastrowid 
        self.conn.commit()

    def delete_task(self,id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (id,))
        self.conn.commit()


    def query(self,filter=None, order=None):
        tasks = []
        sql = "SELECT * FROM tasks"
        if filter is not None:
            sql += " WHERE " + filter
        if order is not None:
            sql += " ORDER BY " + order
        cur = self.conn.cursor()    
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            id, name, description,due_date, priority, status, list_name = row
            task = Task(name, description,due_date, priority, status,list_name)
            task.id = id
            tasks.append(task)
        return tasks

    def update(self,Task):
        self.cur = self.conn.cursor()
        self.cur.execute("""UPDATE tasks SET NAME = ?, description = ?,Due_date = ? , priority = ?, list_name = ?
            WHERE id = ?""", (Task.name,Task.description,Task.due_date,Task.priority,Task.list_name , Task.id))
        self.conn.commit()

    def change_status(self,id,check):
        self.cur = self.conn.cursor()
        if check == True:
            self.cur.execute("""UPDATE tasks SET status = ? WHERE id = ?""", (1, id))
        else:
            self.cur.execute("""UPDATE tasks SET status = ? WHERE id = ?""", (0, id))
        self.conn.commit()

    def time_diff(self,date:str) -> int:
        date = datetime.strptime(date,"%Y-%m-%d").date()
        return (date - datetime.now().date()).days

        
    def get_reminders(self) -> list[Task]:
        tasks = self.query()
        result = []
        for task in tasks:
            if self.time_diff(task.due_date)<=3:
                result.append(task)
        return result

        
    def update_categories(self):
        categories : set[Task] = set()
        tasks = self.query()
        for task in tasks:
            categories.add(task.list_name)
        self.categories_count = len(categories)
        self.categories = categories
