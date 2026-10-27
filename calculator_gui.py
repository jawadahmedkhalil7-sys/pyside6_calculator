
import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QHBoxLayout,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)

from database import save_calculation, get_calculations


class HistoryWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Calculation History")
        self.resize(750, 400)

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "First Number", "Operator",
            "Second Number", "Result", "Date"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        clear_button = QPushButton("Clear All History")
        clear_button.clicked.connect(self.clear_history)
        layout.addWidget(clear_button)

        self.load_history()

    def load_history(self):
        records = get_calculations()

        self.table.setRowCount(len(records))

        for row_index, record in enumerate(records):
            for column_index, value in enumerate(record):
                self.table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(str(value))
                )

    def clear_history(self):
        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Delete all calculation history?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            from database import clear_calculations
            clear_calculations()
            self.load_history()


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Calculator")
        self.resize(360, 500)

        self.first_number = None
        self.pending_operator = None
        self.reset_display = False

        self.build_ui()
        self.apply_style()

    def build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("My Calculator")
        title.setObjectName("title")
        layout.addWidget(title)

        self.display = QLineEdit()
        self.display.setPlaceholderText("0")
        self.display.setMinimumHeight(65)
        self.display.setAlignment(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.AlignmentFlag.AlignRight
        )
        self.display.setText("0")
        layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ("C", 0, 0), ("⌫", 0, 1), ("History", 0, 2), ("/", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("*", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("+/-", 4, 0), ("0", 4, 1), (".", 4, 2), ("=", 4, 3),
        ]

        for text, row, column in buttons:
            button = QPushButton(text)
            button.setMinimumHeight(55)
            button.clicked.connect(
                lambda checked=False, value=text: self.button_clicked(value)
            )
            grid.addWidget(button, row, column)

        layout.addLayout(grid)

    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #20242b;
                color: white;
                font-size: 17px;
            }

            QLabel#title {
                font-size: 26px;
                font-weight: bold;
                padding: 8px;
            }

            QLineEdit {
                background-color: #343a40;
                color: white;
                font-size: 28px;
                padding: 10px;
                border: 2px solid #59636e;
                border-radius: 8px;
            }

            QPushButton {
                background-color: #3b424c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
            }

            QPushButton:hover {
                background-color: #56616e;
            }

            QPushButton:pressed {
                background-color: #2471a3;
            }
        """)

    def button_clicked(self, value):
        if value == "C":
            self.clear_display()

        elif value == "⌫":
            self.backspace()

        elif value == "History":
            dialog = HistoryWindow(self)
            dialog.exec()

        elif value in ["+", "-", "*", "/"]:
            self.choose_operator(value)

        elif value == "=":
            self.calculate_result()

        elif value == "+/-":
            self.change_sign()

        elif value == ".":
            self.add_decimal()

        else:
            self.add_digit(value)

    def add_digit(self, digit):
        current = self.display.text()

        if self.reset_display or current == "0" or current == "Error":
            self.display.setText(digit)
            self.reset_display = False
        else:
            self.display.setText(current + digit)

    def add_decimal(self):
        current = self.display.text()

        if self.reset_display or current == "Error":
            self.display.setText("0.")
            self.reset_display = False
        elif "." not in current:
            self.display.setText(current + ".")

    def clear_display(self):
        self.display.setText("0")
        self.first_number = None
        self.pending_operator = None
        self.reset_display = False

    def backspace(self):
        if self.reset_display:
            return

        current = self.display.text()

        if len(current) > 1:
            new_text = current[:-1]
            if new_text in ["", "-"]:
                new_text = "0"
            self.display.setText(new_text)
        else:
            self.display.setText("0")

    def change_sign(self):
        current = self.display.text()

        if current not in ["0", "Error"]:
            if current.startswith("-"):
                self.display.setText(current[1:])
            else:
                self.display.setText("-" + current)

    def choose_operator(self, operator):
        try:
            current_number = float(self.display.text())
        except ValueError:
            return

        if self.pending_operator is not None and not self.reset_display:
            self.calculate_result()

            if self.display.text() == "Error":
                return

            current_number = float(self.display.text())

        self.first_number = current_number
        self.pending_operator = operator
        self.reset_display = True

    def calculate_result(self):
        if self.pending_operator is None or self.first_number is None:
            return

        try:
            number1 = self.first_number
            number2 = float(self.display.text())
            operator = self.pending_operator

            if operator == "+":
                result = number1 + number2
            elif operator == "-":
                result = number1 - number2
            elif operator == "*":
                result = number1 * number2
            elif operator == "/":
                if number2 == 0:
                    QMessageBox.warning(
                        self, "Math Error", "Cannot divide by zero!"
                    )
                    return
                result = number1 / number2
            else:
                return

            save_calculation(number1, operator, number2, result)

            self.display.setText(str(result))
            self.first_number = None
            self.pending_operator = None
            self.reset_display = True

        except (ValueError, OverflowError) as error:
            QMessageBox.warning(self, "Error", str(error))
        except Exception as error:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not save calculation:\n{error}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
