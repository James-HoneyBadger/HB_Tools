import sys
import csv
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QLineEdit,
    QInputDialog,
    QTextBrowser,
)
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt5.QtCore import QRegExp, Qt, QThread, pyqtSignal


class CommandWorker(QThread):
    finished = pyqtSignal(str, str)  # stdout, stderr

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            result = subprocess.run(
                self.command, shell=True, capture_output=True, text=True, timeout=30
            )
            self.finished.emit(result.stdout, result.stderr)
        except subprocess.TimeoutExpired:
            self.finished.emit("", "Command timed out")
        except Exception as e:
            self.finished.emit("", str(e))


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Define formats
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.blue)
        keyword_format.setFontWeight(QFont.Bold)

        string_format = QTextCharFormat()
        string_format.setForeground(Qt.darkGreen)

        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.gray)
        comment_format.setFontItalic(True)

        # Keywords
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda", "None",
            "nonlocal", "not", "or", "pass", "raise", "return", "True",
            "try", "while", "with", "yield"
        ]

        self.highlighting_rules = []

        # Keyword rules
        for word in keywords:
            pattern = QRegExp(r"\b" + word + r"\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # String rules
        self.highlighting_rules.append((QRegExp(r'".*"'), string_format))
        self.highlighting_rules.append((QRegExp(r"'.*'"), string_format))

        # Comment rules
        self.highlighting_rules.append((QRegExp(r"#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class HBIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HB Tools - PeopleTools IDE Clone")
        self.setGeometry(100, 100, 1200, 800)

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create tabs
        self.create_application_designer_tab()
        self.create_peoplecode_editor_tab()
        self.create_data_mover_tab()
        self.create_query_tool_tab()
        self.create_process_scheduler_tab()

        self.show()

    def create_application_designer_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Toolbar
        toolbar = QHBoxLayout()
        add_label_btn = QPushButton("Add Label")
        add_text_edit_btn = QPushButton("Add Text Edit")
        add_button_btn = QPushButton("Add Button")
        clear_btn = QPushButton("Clear Design")
        save_design_btn = QPushButton("Save Design")
        load_design_btn = QPushButton("Load Design")

        toolbar.addWidget(add_label_btn)
        toolbar.addWidget(add_text_edit_btn)
        toolbar.addWidget(add_button_btn)
        toolbar.addWidget(clear_btn)
        toolbar.addWidget(save_design_btn)
        toolbar.addWidget(load_design_btn)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        # Design area
        self.design_area = QWidget()
        self.design_layout = QVBoxLayout(self.design_area)
        self.design_area.setStyleSheet("border: 1px solid black; background-color: white;")

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.design_area)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Connect buttons
        add_label_btn.clicked.connect(lambda: self.add_component_to_design("label"))
        add_text_edit_btn.clicked.connect(lambda: self.add_component_to_design("text_edit"))
        add_button_btn.clicked.connect(lambda: self.add_component_to_design("button"))
        clear_btn.clicked.connect(self.clear_design)
        save_design_btn.clicked.connect(self.save_design)
        load_design_btn.clicked.connect(self.load_design)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Application Designer")

    def create_peoplecode_editor_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("PeopleCode Editor"))
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText("Write PeopleCode here...")
        self.highlighter = PythonHighlighter(self.code_editor.document())
        layout.addWidget(self.code_editor)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "PeopleCode Editor")

    def create_data_mover_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Toolbar
        toolbar = QHBoxLayout()
        load_csv_btn = QPushButton("Load CSV")
        load_json_btn = QPushButton("Load JSON")
        save_csv_btn = QPushButton("Save CSV")
        save_json_btn = QPushButton("Save JSON")

        toolbar.addWidget(load_csv_btn)
        toolbar.addWidget(load_json_btn)
        toolbar.addWidget(save_csv_btn)
        toolbar.addWidget(save_json_btn)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        # Data table
        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)

        # Connect buttons
        load_csv_btn.clicked.connect(self.load_csv)
        load_json_btn.clicked.connect(self.load_json)
        save_csv_btn.clicked.connect(self.save_csv)
        save_json_btn.clicked.connect(self.save_json)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Data Mover")

    def create_query_tool_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Query builder
        builder_layout = QHBoxLayout()
        builder_layout.addWidget(QLabel("Table:"))
        self.table_combo = QComboBox()
        self.table_combo.addItems(["users", "products", "orders"])
        builder_layout.addWidget(self.table_combo)

        builder_layout.addWidget(QLabel("Columns:"))
        self.columns_edit = QTextEdit()
        self.columns_edit.setMaximumHeight(30)
        self.columns_edit.setPlaceholderText("*")
        builder_layout.addWidget(self.columns_edit)

        generate_btn = QPushButton("Generate SQL")
        builder_layout.addWidget(generate_btn)

        layout.addLayout(builder_layout)

        # SQL Editor
        layout.addWidget(QLabel("SQL Query:"))
        self.sql_editor = QTextEdit()
        self.sql_editor.setPlaceholderText("SELECT * FROM users;")
        layout.addWidget(self.sql_editor)

        # Execute button
        execute_btn = QPushButton("Execute Query")
        layout.addWidget(execute_btn)

        # Results table
        self.query_results = QTableWidget()
        layout.addWidget(self.query_results)

        # Connect
        generate_btn.clicked.connect(self.generate_sql)
        execute_btn.clicked.connect(self.execute_query)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Query Tool")

    def create_process_scheduler_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Add task form
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Name:"))
        self.task_name_edit = QLineEdit()
        form_layout.addWidget(self.task_name_edit)

        form_layout.addWidget(QLabel("Command:"))
        self.task_command_edit = QLineEdit()
        form_layout.addWidget(self.task_command_edit)

        form_layout.addWidget(QLabel("Schedule:"))
        self.schedule_combo = QComboBox()
        self.schedule_combo.addItems(["Manual", "Daily", "Hourly", "Weekly"])
        form_layout.addWidget(self.schedule_combo)

        add_task_btn = QPushButton("Add Task")
        form_layout.addWidget(add_task_btn)

        layout.addLayout(form_layout)

        # Tasks table
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(4)
        self.tasks_table.setHorizontalHeaderLabels(["Name", "Command", "Schedule", "Actions"])
        layout.addWidget(self.tasks_table)

        # Connect
        add_task_btn.clicked.connect(self.add_task)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Process Scheduler")


    def add_component_to_design(self, component_type, text=""):
        if component_type == "label":
            widget = QLabel(text or "New Label")
        elif component_type == "text_edit":
            widget = QTextEdit()
            widget.setMaximumHeight(50)
            if text:
                widget.setPlainText(text)
        elif component_type == "button":
            widget = QPushButton(text or "New Button")
        self.design_layout.addWidget(widget)

    def clear_design(self):
        # Remove all widgets from design layout
        while self.design_layout.count():
            child = self.design_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def save_design(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Design", "", "JSON Files (*.json)")
        if file_path:
            try:
                components = []
                for i in range(self.design_layout.count()):
                    widget = self.design_layout.itemAt(i).widget()
                    if isinstance(widget, QLabel):
                        components.append({"type": "label", "text": widget.text()})
                    elif isinstance(widget, QTextEdit):
                        components.append({"type": "text_edit", "text": widget.toPlainText()})
                    elif isinstance(widget, QPushButton):
                        components.append({"type": "button", "text": widget.text()})
                with open(file_path, 'w') as file:
                    json.dump(components, file, indent=4)
                QMessageBox.information(self, "Success", "Design saved successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save design: {str(e)}")

    def load_design(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Design", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    components = json.load(file)
                self.clear_design()
                for comp in components:
                    self.add_component_to_design(comp["type"], comp.get("text", ""))
                QMessageBox.information(self, "Success", "Design loaded successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load design: {str(e)}")

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    data = list(reader)
                    if not data:
                        QMessageBox.warning(self, "Error", "CSV file is empty")
                        return
                    # Validate consistent columns
                    col_count = len(data[0])
                    for i, row in enumerate(data[1:], 1):
                        if len(row) != col_count:
                            QMessageBox.warning(self, "Error", f"Inconsistent columns at row {i+1}")
                            return
                    self.populate_table(data)
                    QMessageBox.information(self, "Success", f"Loaded {len(data)} rows from CSV")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load CSV: {str(e)}")

    def load_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open JSON", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    if not isinstance(data, list):
                        QMessageBox.warning(self, "Error", "JSON root must be an array")
                        return
                    if not data:
                        QMessageBox.warning(self, "Error", "JSON array is empty")
                        return
                    if not all(isinstance(item, dict) for item in data):
                        QMessageBox.warning(self, "Error", "All items in JSON array must be objects")
                        return
                    # Check consistent keys
                    keys = set(data[0].keys())
                    for i, item in enumerate(data[1:], 1):
                        if set(item.keys()) != keys:
                            QMessageBox.warning(self, "Error", f"Inconsistent keys at item {i+1}")
                            return
                    headers = list(keys)
                    rows = [list(item.values()) for item in data]
                    table_data = [headers] + rows
                    self.populate_table(table_data)
                    QMessageBox.information(self, "Success", f"Loaded {len(data)} records from JSON")
            except json.JSONDecodeError as e:
                QMessageBox.warning(self, "Error", f"Invalid JSON: {str(e)}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load JSON: {str(e)}")

    def save_csv(self):
        if self.data_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No data to save")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    for row in range(self.data_table.rowCount()):
                        row_data = []
                        for col in range(self.data_table.columnCount()):
                            item = self.data_table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                QMessageBox.information(self, "Success", "CSV saved successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save CSV: {str(e)}")

    def save_json(self):
        if self.data_table.rowCount() <= 1:  # No data rows
            QMessageBox.warning(self, "Error", "No data to save")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON Files (*.json)")
        if file_path:
            try:
                headers = []
                for col in range(self.data_table.columnCount()):
                    item = self.data_table.horizontalHeaderItem(col)
                    headers.append(item.text() if item else f"Column {col+1}")

                data = []
                for row in range(1, self.data_table.rowCount()):  # Skip header
                    row_dict = {}
                    for col in range(self.data_table.columnCount()):
                        item = self.data_table.item(row, col)
                        row_dict[headers[col]] = item.text() if item else ""
                    data.append(row_dict)

                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                QMessageBox.information(self, "Success", "JSON saved successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save JSON: {str(e)}")

    def populate_table(self, data):
        if not data:
            return
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(data[0]))
        for row, row_data in enumerate(data):
            for col, cell_data in enumerate(row_data):
                self.data_table.setItem(row, col, QTableWidgetItem(str(cell_data)))
        # Set headers if first row
        if len(data) > 0:
            for col in range(len(data[0])):
                self.data_table.setHorizontalHeaderItem(col, QTableWidgetItem(f"Col {col+1}"))

    def generate_sql(self):
        table = self.table_combo.currentText()
        columns = self.columns_edit.toPlainText().strip() or "*"
        sql = f"SELECT {columns} FROM {table};"
        self.sql_editor.setPlainText(sql)

    def execute_query(self):
        # Mock execution - show sample data based on table
        table = self.table_combo.currentText()
        if table == "users":
            data = [
                ["id", "name", "email"],
                [1, "John Doe", "john@example.com"],
                [2, "Jane Smith", "jane@example.com"]
            ]
        elif table == "products":
            data = [
                ["id", "name", "price"],
                [1, "Widget", "10.99"],
                [2, "Gadget", "25.50"]
            ]
        elif table == "orders":
            data = [
                ["id", "user_id", "product_id", "quantity"],
                [1, 1, 1, 2],
                [2, 2, 2, 1]
            ]
        else:
            data = [["No data"]]
        self.populate_query_results(data)

    def populate_query_results(self, data):
        if not data:
            return
        self.query_results.setRowCount(len(data))
        self.query_results.setColumnCount(len(data[0]))
        for row, row_data in enumerate(data):
            for col, cell_data in enumerate(row_data):
                self.query_results.setItem(row, col, QTableWidgetItem(str(cell_data)))
        # Set headers
        if len(data) > 0:
            for col in range(len(data[0])):
                self.query_results.setHorizontalHeaderItem(col, QTableWidgetItem(data[0][col] if row == 0 else f"Col {col+1}"))

    def add_task(self):
        name = self.task_name_edit.text().strip()
        command = self.task_command_edit.text().strip()
        schedule = self.schedule_combo.currentText()
        if not name or not command:
            QMessageBox.warning(self, "Error", "Name and Command are required")
            return

        row_count = self.tasks_table.rowCount()
        self.tasks_table.insertRow(row_count)
        self.tasks_table.setItem(row_count, 0, QTableWidgetItem(name))
        self.tasks_table.setItem(row_count, 1, QTableWidgetItem(command))
        self.tasks_table.setItem(row_count, 2, QTableWidgetItem(schedule))

        # Add run button
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(lambda: self.run_task(command))
        self.tasks_table.setCellWidget(row_count, 3, run_btn)

        # Clear form
        self.task_name_edit.clear()
        self.task_command_edit.clear()

    def run_task(self, command):
        # Run command in background thread
        self.worker = CommandWorker(command)
        self.worker.finished.connect(self.on_command_finished)
        self.worker.start()

    def on_command_finished(self, stdout, stderr):
        if stderr:
            QMessageBox.warning(self, "Command Error", f"Stderr: {stderr}")
        else:
            QMessageBox.information(self, "Command Success", f"Output: {stdout}")


def main():
    app = QApplication(sys.argv)
    HBIDE()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
