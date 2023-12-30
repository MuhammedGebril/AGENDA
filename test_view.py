# test_myapp.py
import pytest
from kivy.uix.textinput import TextInput
from view import View, DialogContent


class MockedDialogContent(DialogContent):
    """Mocked version of DialogContent with date_text attribute."""

    def __init__(self, **kwargs):
        # Correct way to call super constructor in Kivy
        super(DialogContent, self).__init__(**kwargs)
        self.ids.date_text = TextInput(text="mocked_date")


@pytest.fixture
def app():
    # Create an instance of the app for testing
    app = View(controller=None)
    app.build()
    return app


def test_dialog_content_defaults():
    # Test if MockedDialogContent initializes correctly
    dialog_content = MockedDialogContent()
    assert dialog_content.ids.date_text.text == "mocked_date"



