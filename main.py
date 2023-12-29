# main.py
from view import View
from task_controller import TaskController
from task_model import TaskModel

# Instantiate the model, view, and controller
if __name__ == "__main__":
    task_model = TaskModel()
    task_controller = TaskController(view=None, model=task_model)
    
    # Pass the initialized controller to the view
    task_view = View(controller=task_controller)
    
    task_controller.view = task_view  # Set the view in the controller

    task_controller.run()