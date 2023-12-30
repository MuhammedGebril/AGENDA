from task import Task
from datetime import datetime

class TaskController:
    def __init__(self, view, model):
        self.view = view
        self.model = model


    def run(self):
        self.view.run()
        pass

    def add_task(self, task_name,description=None,task_date = datetime.now().strftime("%Y-%m-%d"),priority=0,list_name="General"):
        if list_name.text not in self.model.categories and self.model.categories_count == 10:
            return False
        '''Add task to the list of tasks'''
        if list_name.text == '':
            list_name.text = 'General'
        self.model.add_task(Task (task_name.text,description.text,task_date.text,priority.text,0,list_name.text))

        #Clearing Dialog Fields
        task_name.text = ''
        task_date.text=str(datetime.now().strftime("%Y-%m-%d"))
        description.text=''
        priority.text=''
        self.update_view()
    

    def delete_task(self,id):
        self.model.delete_task(id)
        self.update_view()
    
    def due_today(self):
        return self.model.query("Due_Date = '"+str(datetime.now().strftime("%Y-%m-%d")+"'" ))
    
    def all_tasks(self):
        return self.model.query()
    
    def reminders(self):
        return self.model.get_reminders()

    def get_task(self,id):
        query="id= '"+str(id)+"'"
        return self.model.query(query)        
    
    def mark(self,id,check):
        self.model.change_status(id,check)
        self.update_view()

    def update_view(self):
        if self.view.selected_item == 1:
            self.view.update_daily_tasks()
        elif self.view.selected_item == 2:
            self.view.update_all_tasks()
        elif self.view.selected_item == 3:
            self.view.view_categories()
        elif self.view.selected_item == 4:
            self.view.update_reminders()
        elif self.view.selected_item == 5:
            self.view.update_about()

    def get_categories(self):
        self.model.update_categories()
        return list(self.model.categories)

    def category_tasks(self,list_name):
        query = "List_Name = "+'"'+list_name+'"'
        return self.model.query(query)
        
    def update_task(self, task_name,description=None,task_date = datetime.now().strftime("%Y-%m-%d"),priority=0,list_name="General"):
        if list_name.text not in self.model.categories and self.model.categories_count == 10:
            return False
        '''Add task to the list of tasks'''
        if list_name.text == '':
            list_name.text = 'General'
        task = Task (task_name.text,description.text,task_date.text,priority.text,0,list_name.text)
        task.id = self.view.general_task_id
        self.model.update(task)
        #Clearing Dialog Fields
        task_name.text = ''
        task_date.text=str(datetime.now().strftime("%Y-%m-%d"))
        description.text=''
        priority.text=''
        self.view.list_categories=self.model.update_categories()
        self.update_view()
