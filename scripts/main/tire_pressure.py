from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class TirePressureWidget(QWidget):
    def __init__(self, tire_name, pressure=0.0, parent=None):
        super().__init__(parent)
        self.tire_name = tire_name
        self.pressure = pressure
        self.initUI()

    def initUI(self):
        # Criar um QFrame estilizado como os outros widgets
        frame = QFrame(self)
        frame.setStyleSheet("background-color: #303030; padding: 10px; border-radius: 15px;")
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        # Nome do pneu
        name_label = QLabel(self.tire_name, self)
        name_label.setFont(QFont("High Speed", 14))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #DFAE21;")  # Cor consistente com os botões

        # Pressão do pneu
        self.pressure_label = QLabel(f"{self.pressure:.1f} bar", self)
        self.pressure_label.setFont(QFont("High Speed", 16))
        self.pressure_label.setAlignment(Qt.AlignCenter)
        self.pressure_label.setStyleSheet("color: white;")

        # Adicionar ao layout
        layout.addWidget(name_label)
        layout.addWidget(self.pressure_label)

        # Layout principal do widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        main_layout.setContentsMargins(0, 0, 0, 0)

    def set_pressure(self, pressure):
        """Atualiza a pressão exibida no widget."""
        self.pressure = pressure
        self.pressure_label.setText(f"{self.pressure:.1f} bar")