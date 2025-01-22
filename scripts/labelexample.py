# Importação de Bibliotecas: PyQt6.QtWidgets possibilitam a parte funcional da dash, Matplotlib permite criação de gráficos dinâmicos

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, 
    QWidget, QComboBox, QCheckBox, QRadioButton, QSlider, QProgressBar, 
    QSpinBox, QDateEdit, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime

# Classe principal da janela principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Exemplo Funcional")
        self.setGeometry(100, 100, 800, 800)

        # Stylesheet tema escuro
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            QLineEdit, QComboBox, QCheckBox, QRadioButton, QSlider, QProgressBar, QSpinBox, QDateEdit, QTableWidget {
                background-color: #3e3e3e;
                border: 1px solid #f0f0f0;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #4e4e4e;
                border: 1px solid #f0f0f0;
                color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #5e5e5e;
            }
            QHeaderView::section {
                background-color: #3e3e3e;
                color: #f0f0f0;
                border: 1px solid #f0f0f0;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #4e4e4e;
            }
        """)

        # Cria widget central e inicia layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Exemplo QLabel 
        self.label = QLabel("Exemplo de QLabel")
        layout.addWidget(self.label)

        # Exemplo QLineEdit 
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Digite algo aqui...")
        layout.addWidget(self.line_edit)

        # Exemplo QPushButton 
        button = QPushButton("Me clica! Me clica!")
        button.clicked.connect(self.update_label)
        layout.addWidget(button)

        # Exemplo QComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Opção 1", "Opção 2", "Opção 3"])
        self.combo_box.currentTextChanged.connect(self.update_label_with_combo)
        layout.addWidget(self.combo_box)

        # Exemplo QCheckBox
        self.check_box = QCheckBox("Marca eu!")
        self.check_box.stateChanged.connect(self.update_label_with_check)
        layout.addWidget(self.check_box)

        # Exemplo QRadioButton
        self.radio_button = QRadioButton("Seleciona eu!")
        self.radio_button.toggled.connect(self.update_label_with_radio)
        layout.addWidget(self.radio_button)

        # Exemplo QSlider 
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.update_label_with_slider)
        layout.addWidget(self.slider)

        # Exemplo QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # QPushButton para aumentar QProgressBar
        progress_button = QPushButton("Atualizar progresso")
        progress_button.clicked.connect(self.update_progress_bar)
        layout.addWidget(progress_button)

        # Exemplo QSpinBox
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        self.spin_box.valueChanged.connect(self.update_label_with_spinbox)
        layout.addWidget(self.spin_box)

        # Exemplo QDateEdit
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.dateChanged.connect(self.update_label_with_date)
        layout.addWidget(self.date_edit)

        # Exemplo QTableWidget
        self.table_widget = QTableWidget(3, 3)
        self.table_widget.setHorizontalHeaderLabels(["Coluna 1", "Coluna 2", "Coluna 3"])
        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem(f"Item {row+1}, {col+1}")
                self.table_widget.setItem(row, col, item)
        layout.addWidget(self.table_widget)

        # Exemplo gráfico Matplotlib
        self.figure, self.ax = plt.subplots()
        self.figure.patch.set_facecolor('#2e2e2e')
        self.ax.set_facecolor('#2e2e2e')
        self.ax.spines['bottom'].set_color('#f0f0f0')
        self.ax.spines['top'].set_color('#f0f0f0')
        self.ax.spines['right'].set_color('#f0f0f0')
        self.ax.spines['left'].set_color('#f0f0f0')
        self.ax.xaxis.label.set_color('#f0f0f0')
        self.ax.yaxis.label.set_color('#f0f0f0')
        self.ax.tick_params(axis='x', colors='#f0f0f0')
        self.ax.tick_params(axis='y', colors='#f0f0f0')
        self.ax.title.set_color('#f0f0f0')
        self.canvas = FigureCanvas(self.figure)
        self.plot_graph()
        layout.addWidget(self.canvas)

        # Set the layout to the central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_label(self):
        text = self.line_edit.text()
        self.label.setText(f"Voce digitou: {text}")

    def update_label_with_combo(self, text):
        self.label.setText(f"Selecionado: {text}")

    def update_label_with_check(self):
        state = "Checado" if self.check_box.isChecked() else "Não-Checado"
        self.label.setText(f"CheckBox está {state}")

    def update_label_with_radio(self):
        state = "Selececionado" if self.radio_button.isChecked() else "Não Selecionado"
        self.label.setText(f"RadioButton está {state}")

    def update_label_with_slider(self):
        value = self.slider.value()
        self.label.setText(f"Valor do Slider: {value}")

    def update_progress_bar(self):
        value = self.slider.value()
        self.progress_bar.setValue(value)

    def update_label_with_spinbox(self):
        value = self.spin_box.value()
        self.label.setText(f"Valor SpinBox: {value}")

    def update_label_with_date(self, date):
        self.label.setText(f"Data selecionada: {date.toString()}")

    def plot_graph(self):
        x = [1, 2, 3, 4, 5]
        y = [10, 20, 15, 30, 25]
        self.ax.clear()
        self.ax.plot(x, y, marker='o', color='#f0f0f0')
        self.ax.set_title("Gráfico Exemplo")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
