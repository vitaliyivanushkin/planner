import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QLabel, QMessageBox, QDateEdit, QListWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description="", due_date=None):
        self.tasks.append({"title": title, "description": description, "completed": False, "due_date": due_date})

    def view_tasks(self):
        return self.tasks

    def mark_completed(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]["completed"] = True

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)

    def save_tasks(self, filename="tasks.json"):
        with open(filename, "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self, filename="tasks.json"):
        try:
            with open(filename, "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.todo_list = ToDoList()
        self.todo_list.load_tasks()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('To-Do List App')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText('Enter task title')
        layout.addWidget(self.task_input)

        self.desc_input = QLineEdit(self)
        self.desc_input.setPlaceholderText('Enter task description (optional)')
        layout.addWidget(self.desc_input)

        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        add_button = QPushButton('Add Task', self)
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)

        button_layout = QHBoxLayout()

        complete_button = QPushButton('Mark Completed', self)
        complete_button.clicked.connect(self.mark_completed)
        button_layout.addWidget(complete_button)

        delete_button = QPushButton('Delete Task', self)
        delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.update_task_list()

    def add_task(self):
        title = self.task_input.text()
        description = self.desc_input.text()
        due_date = self.date_input.date().toString("yyyy-MM-dd")
        if title:
            self.todo_list.add_task(title, description, due_date)
            self.update_task_list()
            self.task_input.clear()
            self.desc_input.clear()
            self.todo_list.save_tasks()
        else:
            QMessageBox.warning(self, 'Error', 'Task title cannot be empty')

    def update_task_list(self):
        self.task_list.clear()
        for idx, task in enumerate(self.todo_list.view_tasks()):
            status = "Done" if task["completed"] else "Not Done"
            due_date = task.get("due_date", "No due date")
            item_text = f"{idx + 1}. {task['title']} - {status}\n {task['description']}\n Due: {due_date}"
            item = QListWidgetItem(item_text)
            if not task["completed"]:
                item.setForeground(QColor('red'))
            self.task_list.addItem(item)

    def mark_completed(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            task_index = self.task_list.row(selected_item)
            self.todo_list.mark_completed(task_index)
            self.update_task_list()
            self.todo_list.save_tasks()

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            task_index = self.task_list.row(selected_item)
            self.todo_list.delete_task(task_index)
            self.update_task_list()
            self.todo_list.save_tasks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ToDoApp()
    ex.show()
    sys.exit(app.exec_())

