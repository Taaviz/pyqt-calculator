
from PyQt5.QtWidgets import (QWidget, QLabel, QWIDGETSIZE_MAX, QVBoxLayout,
                             QGridLayout, QPushButton, QSizePolicy)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Calculadora(QWidget):


    # CONSTRUCTOR - INITIALIZING ATTRIBUTES
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Calculadora")
        self.setWindowIcon(QIcon("../assets/calc.png"))
        self.setGeometry(780, 300, 290, 460)
        self.equac_label = QLabel("", self)
        self.num_label = QLabel("0", self)
        self.chars = []
        self.all_chars = []
        self.resu = 0
        self.zero_div = 0
        self.last_op = ""
        self.initUI()


    # CREATE RESPONSIVE GRID BUTTONS - AND YOUR CONNECTION (CALL display_calc)
    def create_buttons(self, layout):

        buttons = ["AC", "+/-", "%", "÷",
                  "7", "8", "9", "×",
                  "4", "5", "6", "-",
                  "1", "2", "3", "+",
                  "0", ".", "⌫", "="
                  ]

        row = 0
        column = 0
        for button in buttons:

            btn = QPushButton(button, self)

            btn.clicked.connect(lambda _, name=button: self.display_calc(name))

            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            btn.setMinimumSize(70, 70)

            main_style = """
            QPushButton {
                font-size: 25px;
                font-family: Arial;
                border: none;
                outline: none;
            }
            """

            if button in ['AC', '+/-', '%', '÷', '×', '-', '+']:
                btn.setStyleSheet(main_style + """
                    QPushButton {
                        background-color: #6D728C;
                        color: #F23568;
                    }
                    QPushButton:hover {
                        background-color: #5f647a;
                    }
                    QPushButton:pressed {
                        background-color: #464a5c;
                    }
                """)

            elif button in ['=']:
                btn.setStyleSheet(main_style + """
                    QPushButton {
                        background-color: #F23568;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #c72450;
                    }
                    QPushButton:pressed {
                        background-color: #a81d42;
                    }
                """)
            else:

                btn.setStyleSheet(main_style + """
                    QPushButton {
                        background-color: #393E59;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #4e557a;
                    }
                    QPushButton:pressed {
                        background-color: #393E59;
                    }
                """)

            layout.addWidget(btn, row, column)

            column += 1
            if column > 3:
                row += 1
                column = 0


    # INITIALIZE WIDGETS IN UI (CALL create_buttons)
    def initUI(self):

        vbox = QVBoxLayout()

        vbox.setSpacing(0)

        vbox.addWidget(self.equac_label)
        vbox.addWidget(self.num_label)

        self.setObjectName("JanelaPrincipal")
        self.num_label.setObjectName("num_label")
        self.equac_label.setObjectName("equac_label")

        self.setStyleSheet("""
            QWidget#JanelaPrincipal {
                background-color: #242B4C;
            }
            QLabel {
                background-color: #323A59;
                font-family: Arial;
            }
            QLabel#num_label {
                font-size: 75px;
                color: white;
                border: 0px;
            }
            QLabel#equac_label {
                font-size: 22px;
                color: #959DAF;
                border: 0px;
            }
        """)

        self.equac_label.setContentsMargins(0, 0, 10, 0)
        self.num_label.setContentsMargins(0, 0, 10, 0)

        self.equac_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.num_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.equac_label.setMaximumSize(QWIDGETSIZE_MAX, 50)
        self.num_label.setMinimumSize(290, 100)

        gbox = QGridLayout()

        self.create_buttons(gbox)

        gbox.setSpacing(2)

        main_vbox = QVBoxLayout()

        main_vbox.addLayout(vbox, 1)
        main_vbox.addLayout(gbox, 2)

        main_vbox.setSpacing(2)

        self.setLayout(main_vbox)

        main_vbox.setContentsMargins(4, 4, 4, 4)


    # DISPLAY CHARACTERS OF BUTTONS - AND CALCULUS - IN LABELS (CALL operations)
    def display_calc(self, char):

        if ' = ' in self.all_chars and char:
            self.chars.clear()
            self.num_label.setText("0")
            self.equac_label.setText("")
            self.all_chars.clear()
            self.resu = 0
            self.zero_div = 0
            self.last_op = ""
            self.num_label.setStyleSheet("font-size: 75px;")

        if self.chars and char == '⌫':
            self.chars.pop()

            if not self.chars or self.chars == ['-'] or self.chars == ['0']:
                self.num_label.setText("0")
                self.chars.clear()

            else:
                self.num_label.setText("".join(self.chars))

        elif char == 'AC':
            self.chars.clear()
            self.num_label.setText("0")
            self.equac_label.setText("")
            self.all_chars.clear()
            self.resu = 0
            self.zero_div = 0
            self.last_op = ""
            self.num_label.setStyleSheet("font-size: 75px;")

        elif self.chars and char == '+/-':

            if self.chars[0] == '-':
                self.chars.pop(0)
            else:
                self.chars.insert(0, '-')

            self.num_label.setText("".join(self.chars))

        elif self.chars and char == '%':
            is_integer = self.is_int("".join(self.chars))

            if is_integer:
                valor = int("".join(self.chars))
            else:
                valor = float("".join(self.chars))

            if self.last_op in '+-':
                perc = self.resu * (valor / 100)
            elif self.last_op in '×÷':
                perc = valor / 100

            self.chars = list(str(perc))

            self.num_label.setText(str(perc))

        elif char.isdigit() or char == '.':

            if (self.chars and char != '.') or (char != '0' and char != '.'):
                self.chars.append(char)
                self.num_label.setText("".join(self.chars))

            elif self.chars and char == '.' and self.chars.count('.') == 0:
                self.chars.append('.')
                self.num_label.setText("".join(self.chars))

            elif not self.chars and char == '.':
                self.chars.append('0')
                self.chars.append('.')

                self.num_label.setText("".join(self.chars))

        elif char in '+-×÷=':

            if self.chars:
                is_integer = self.is_int("".join(self.chars))

                if is_integer:
                    current_number = int("".join(self.chars))
                else:
                    current_number = float("".join(self.chars))

                if self.last_op:
                    self.operations(self.last_op, current_number)
                else:
                    self.resu = current_number

                self.last_op = char if char != '=' else ''

                if self.last_op and char != '=':
                    self.all_chars = list(str(self.resu))
                    self.all_chars.append(f" {char} ")

                else:
                    self.all_chars += self.chars
                    self.all_chars.append(f" {char} ")

                if char == '=':

                    if self.zero_div != 1:
                        self.equac_label.setText(f"{"".join(self.all_chars)}".strip())
                        self.num_label.setText(f"{self.resu}")

                    else:
                        self.num_label.setText("Divisão por zero!")
                        self.num_label.setStyleSheet("font-size: 40px;")

                else:
                    self.equac_label.setText(f"{self.resu} {char}".strip())
                    self.num_label.setText("0")

                self.chars.clear()

            elif self.last_op and char != self.last_op and char in '+-×÷':
                self.last_op = char

                self.all_chars[-1] = f" {char} "

                self.equac_label.setText(f"{"".join(self.all_chars)}".strip())


    # REALIZE ALL OPERATIONS AVAILABLE IN UI
    def operations(self, operator, number):

        if operator == '+':
            self.resu += number

        elif operator == '-':
            self.resu -= number

        elif operator == '×':
            self.resu *= number

        elif operator == '÷':
            try:
                self.resu /= number

            except ZeroDivisionError:
                self.zero_div = 1


    # TEST IF A NUMBER IS INT OR FLOAT
    @staticmethod
    def is_int(string):

        try:
            int(string)
            return True

        except ValueError:
            return False
