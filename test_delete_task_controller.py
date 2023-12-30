import unittest
from unittest.mock import MagicMock
from datetime import datetime
from task_controller import TaskController

class TestTaskController(unittest.TestCase):

    def setUp(self):
        # Create mock objects for TaskModel and View
        self.task_model = MagicMock()
        self.view = MagicMock()

        # Create an instance of TaskController with mock objects
        self.task_controller = TaskController(view=self.view, model=self.task_model)

    def test_delete_task(self):
        # Set up test data
        task_id = 123  # Replace with a valid task ID

        # Call the delete_task method
        self.task_controller.delete_task(task_id)

        # Verify that delete_task was called on the TaskModel with the correct argument
        self.task_model.delete_task.assert_called_once_with(task_id)

        # Verify that update_daily_tasks was called on the View
        self.view.update_daily_tasks.assert_called_once()

