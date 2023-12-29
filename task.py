from datetime import datetime 

class Task:
    id = None
    def __init__(self,name,description="No description" , due_date = datetime.now().strftime("%Y-%m-%d")
 ,priority = 0,status:bool =0 ,list_name = "General"):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.list_name = list_name

