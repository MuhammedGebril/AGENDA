# Dependencies
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.chip import MDChip
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineAvatarIconListItem,ThreeLineRightIconListItem,ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime

from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer

from kivymd.uix.label.label import MDLabel



class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self,categories, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime("%Y-%m-%d"))
        self.list_categories = categories


    def on_save(self, instance, value, date_range):
        date = value.strftime("%Y-%m-%d")
        self.ids.date_text.text = str(date)

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def show_priority_menu(self, widget, text_input):
        menu_items = [
            {"text": "Low", "viewclass": "OneLineListItem",
             "on_release": lambda x="Low": self.menu_callback(text_input, x)},
            {"text": "Medium", "viewclass": "OneLineListItem",
             "on_release": lambda x="Medium": self.menu_callback(text_input, x)},
            {"text": "High", "viewclass": "OneLineListItem",
             "on_release": lambda x="High": self.menu_callback(text_input, x)},
        ]
        self.menu = MDDropdownMenu(
            caller=widget,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, text_input, text_item):
        text_input.text = text_item
        if self.menu:
            self.menu.dismiss()

 #############################################################################
    def show_category_menu(self, widget, text_input, categories):
        for i in range(len(categories)):
            menu_items = [{"text": categories[i], "viewclass": "OneLineListItem",
                           "on_release": lambda x=categories[i]: self.menu_callback2(text_input, x)}]
        self.menu2 = MDDropdownMenu(
            caller=widget,
            items=menu_items,
            width_mult=4,
        )
        self.menu2.open()

    def menu_callback2(self, text_input, text_item):
        text_input.text = text_item
        if self.menu2:
            self.menu2.dismiss()
 #############################################################################





##############################################################
class UpdateDialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self,categories,task, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = task.due_date
        self.ids.task_name.text = task.name
        self.ids.task_description.text = task.description
        self.ids.priority_text.text = task.priority
        self.ids.list_name.text = task.list_name
        self.list_categories = categories


    def on_save(self, instance, value, date_range):
        date = value.strftime("%Y-%m-%d")
        self.ids.date_text.text = str(date)

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def show_priority_menu(self, widget, text_input):
        menu_items = [
            {"text": "Low", "viewclass": "OneLineListItem",
             "on_release": lambda x="Low": self.menu_callback(text_input, x)},
            {"text": "Medium", "viewclass": "OneLineListItem",
             "on_release": lambda x="Medium": self.menu_callback(text_input, x)},
            {"text": "High", "viewclass": "OneLineListItem",
             "on_release": lambda x="High": self.menu_callback(text_input, x)},
        ]
        self.menu = MDDropdownMenu(
            caller=widget,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, text_input, text_item):
        text_input.text = text_item
        if self.menu:
            self.menu.dismiss()

 #############################################################################
    def show_category_menu(self, widget, text_input, categories):
        for i in range(len(categories)):
            menu_items = [{"text": categories[i], "viewclass": "OneLineListItem",
                           "on_release": lambda x=categories[i]: self.menu_callback2(text_input, x)}]
        self.menu2 = MDDropdownMenu(
            caller=widget,
            items=menu_items,
            width_mult=4,
        )
        self.menu2.open()

    def menu_callback2(self, text_input, text_item):
        text_input.text = text_item
        if self.menu2:
            self.menu2.dismiss()
#############################################################################



class ListItemWithCheckbox(ThreeLineRightIconListItem):
    '''Custom list item'''

    def __init__(self,task, **kwargs):
        super().__init__(**kwargs)
        self.pk = task.id
        self.text = task.name
        self.secondary_text =task.description
        self.tertiary_text= task.due_date
        



class View(MDApp):
    task_list_dialog = None
    def __init__(self,controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.selected_item = 1
        self.general_task_id =''
        self.list_categories =self.controller.get_categories()
        self.icon = 'proj_icon.png'
        
    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "Pink"
        self.title = "Agenda"
        
    # Showing the task dialog to add tasks 
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                type="custom",
                content_cls=DialogContent(self.list_categories),
            )
        self.task_list_dialog.open()


    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()
        self.task_list_dialog = None

    def on_start(self):
        self.update_daily_tasks()

    #Update the daily tasks on refresh
    def update_daily_tasks(self):
        self.root.ids.container.clear_widgets()
        self.due_today_tasks = self.controller.due_today()
        for task in self.due_today_tasks:
            temp = ListItemWithCheckbox(task)
            if task.status == 1:
                temp.text = '[s]'+temp.text+'[/s]'
                temp.ids.check.active=True
            else:
                temp.text = temp.text
            
            #changing colors of passed dates
            if (datetime.strptime(temp.tertiary_text, '%Y-%m-%d').date()<datetime.today().date()):
                temp.tertiary_text = '[color=#ff0000]'+temp.tertiary_text+'[/color]'
            else:
                temp.tertiary_text = temp.tertiary_text
            self.root.ids.container.add_widget(temp)

    def update_nav_drawer(self,item_id,nav_icon):
        self.root.ids.about_label.opacity=0
        list_items = ['AGENDA','Due Today','All Tasks','Categories','Reminders','About']
        #Resets background colors
        for child in self.root.ids.nav_bar.children[1:]:
            child.bg_color = self.root.ids.nav_drawer.md_bg_color
        #Resets text colors
        for i in range(1,len(self.root.ids.nav_bar.children)-1):
            getattr(self.root.ids,f'nav_icon_{i}').text_color = '#000000'
            getattr(self.root.ids,f'item_{i}').text = list_items[i]
        #Highlight the choosen item and change colors
        getattr(self.root.ids, item_id).bg_color = "#F2B5D4"
        getattr(self.root.ids, item_id).text_color = 1,1,1,1
        getattr(self.root.ids, nav_icon).text_color = '#ffffff'
        getattr(self.root.ids, item_id).text = '[color=#ffffff]'+getattr(self.root.ids, item_id).text+'[/color]'
        self.root.ids.subtitle.text = "[size=40][b]Today Tasks[/b][/size]"

    def update_all_tasks(self):
        self.root.ids.container.clear_widgets()
        self.all_tasks = self.controller.all_tasks()
        for task in self.all_tasks:
            temp = ListItemWithCheckbox(task)
            if task.status == 1:
                temp.text = '[s]'+temp.text+'[/s]'
                temp.ids.check.active=True
            else:
                temp.text = temp.text
            
            #changing colors of passed dates
            if (datetime.strptime(temp.tertiary_text, '%Y-%m-%d').date()<datetime.today().date()):
                temp.tertiary_text = '[color=#ff0000]'+temp.tertiary_text+'[/color]'
            else:
                temp.tertiary_text = temp.tertiary_text
            self.root.ids.container.add_widget(temp)
        self.root.ids.subtitle.text = "[size=40][b]All Tasks[/b][/size]"
        
    def update_selected_item(self,item):
        self.selected_item = item

    def view_categories(self):
        # Clear existing widgets in the container
        self.list_categories = self.controller.get_categories()
        self.root.ids.container.clear_widgets()
        self.root.ids.subtitle.text = "[size=40][b]Categories[/b][/size]"

        # Create a new GridLayout for categories
        categories_layout = GridLayout(
            cols=5,
            # spacing=dp(5),
            #row_force_default=True,
            # col_force_default=True,
            spacing=[dp(180), dp(200)],
            size_hint=(1, None),
            height=self.root.height - dp(50),  # Adjust the height as needed
            width = 500,
            #col_default_width=self.root.width/2
            # row_default_height=100,
            # minimum_width=self.root.ids.container.width,
        )
        categories_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Add widgets to the new GridLayout (customize as needed)
        for i in range(len(self.list_categories)):
            category_button = MDChip(
                text=self.list_categories[i],
                size_hint=(None,None),
                height=200,
                width=500,
                on_release = lambda instance: self.view_selected_category(instance.text)
            )
            setattr(category_button,'id',category_button.text+'_id')
            categories_layout.add_widget(category_button)
        # Append the new GridLayout to the container
        self.root.ids.container.add_widget(categories_layout)


    def view_selected_category(self,list_name:str):
        print(list_name)
        self.root.ids.container.clear_widgets()
        self.root.ids.subtitle.text = "[size=40][b]"+list_name+"[/b][/size]"
        self.category_tasks = self.controller.category_tasks(list_name)
        for task in self.category_tasks:
            temp = ListItemWithCheckbox(task)
            if task.status == 1:
                temp.text = '[s]'+temp.text+'[/s]'
                temp.ids.check.active=True
            else:
                temp.text = temp.text
            
            #changing colors of passed dates
            if (datetime.strptime(temp.tertiary_text, '%Y-%m-%d').date()<datetime.today().date()):
                temp.tertiary_text = '[color=#ff0000]'+temp.tertiary_text+'[/color]'
            else:
                temp.tertiary_text = temp.tertiary_text
            self.root.ids.container.add_widget(temp)



    

    def update_reminders(self):
        self.root.ids.container.clear_widgets()
        self.root.ids.subtitle.text = "[size=40][b]Reminders![/b][/size]"
        self.reminders = self.controller.reminders()
        for task in self.reminders:
            temp = ListItemWithCheckbox(task)
            if task.status == 1:
                temp.text = '[s]'+temp.text+'[/s]'
                temp.ids.check.active=True
            else:
                temp.text = temp.text
            self.root.ids.container.add_widget(temp)

    def update_about(self):
        self.root.ids.container.clear_widgets()
        self.root.ids.subtitle.text = "[size=40][b]About[/b][/size]"
        setattr(self.root.ids.about_label,'label','True')
        about_text = '''
                [size=30][b]About the application:\n[/size]
                [size=20][b]-Task Management application created by students of Faculty of engineering,Alexandria UNI\n[/size]
                [size=20][b]-Helps the user to Organize, Categorize and keep tracking of his tasks\n[/size]
                [size=20][b]-User Friendly and easy to use\n[/size]
                [size=20][b]-Have Reminders to remind the user with tasks with deadline withtin 3 days\n[/size]
                [size=20][b]-Past due tasks are with red\n[/size]
                [size=30][b]Creators:\n[/size]
                [size=20][b]Hazem Mohamed Abdallah\n[/size]
                [size=20][b]Mohamed Gebril Mohamed\n[/size]
                [size=20][b]Nour Hamdy Mohamed\n[/size]
                '''
        setattr(self.root.ids.about_label,'text',str(about_text))
        self.root.ids.about_label.opacity=1


    def show_update_dialog(self,pk):
        tasks = self.controller.get_task(pk)
        task = tasks[0]
        self.general_task_id=task.id
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                type="custom",
                content_cls=UpdateDialogContent(self.list_categories,task),
            )
        self.task_list_dialog.open()
