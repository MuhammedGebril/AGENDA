import unittest
from unittest.mock import MagicMock
from task_controller import TaskController

class TestTaskController(unittest.TestCase):

    def setUp(self):
        # Create mock objects for TaskModel and View
        self.task_model = MagicMock()
        self.view = MagicMock()

        # Create an instance of TaskController with mock objects
        self.task_controller = TaskController(view=self.view, model=self.task_model)

    def test_mark(self):
        # Set up test data
        task_id = 1
        check_value = True

        # Call the mark method
        self.task_controller.mark(task_id, check_value)

        # Verify that change_status was called on the TaskModel with the correct arguments
        self.task_model.change_status.assert_called_once_with(task_id, check_value)

        # Verify that update_daily_tasks was called on the View
        self.view.update_daily_tasks.assert_called_once()

