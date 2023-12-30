from unittest.mock import MagicMock
from task_controller import TaskController
from task_model import TaskModel  # Import your actual model class


class TestTaskController:
    def setup_method(self):
        # Create a mock for the model
        model_mock = MagicMock(spec=TaskModel)

        # Create a mock for the view
        view_mock = MagicMock()

        # Create TaskController with the mock model and view
        self.task_controller = TaskController(view=view_mock, model=model_mock)

    def test_add_task(self):
        # Set up test data
        task_name = MagicMock()
        task_description = MagicMock()
        task_date = MagicMock()
        task_priority = MagicMock()

        # Call the add_task method
        self.task_controller.add_task(task_name, task_description, task_date, task_priority)

        # Add assertions as needed
        self.task_controller.view.update_daily_tasks.assert_called_once()
