import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from task_controller import TaskController

class TestTaskController(unittest.TestCase):

    def setUp(self):
        # Create mock objects for TaskModel and View
        self.task_model = MagicMock()
        self.view = MagicMock()

        # Create an instance of TaskController with mock objects
        self.task_controller = TaskController(view=self.view, model=self.task_model)

    def test_due_today(self):
        # Set up test data
        mock_datetime = datetime(2023, 12, 26)
        with patch('task_controller.datetime', MagicMock(now=MagicMock(return_value=mock_datetime))):
            # Call the due_today method
            self.task_controller.due_today()

        # Verify that query was called on the TaskModel with the correct argument
        self.task_model.query.assert_called_once_with("Due_Date = '2023-12-26'")


