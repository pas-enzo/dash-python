from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPainterPath

class PacmanButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumSize(150, 150)
        self.setStyleSheet("border-radius: 75px; background-color: green;")
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw Pac-Man body with mouth as a sector cut
        painter.setBrush(QBrush(Qt.yellow))
        path = QPainterPath()
        path.moveTo(75, 75)
        path.arcTo(20, 20, 110, 110, 30, 300)  # Creates a sector
        path.closeSubpath()
        painter.drawPath(path)
        
        # Draw eye
        painter.setBrush(QBrush(Qt.black))
        painter.drawEllipse(80, 40, 10, 10)

class CallCarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("Chamar Carro para o Box")
        self.label.setStyleSheet("font-size: 20px; color: black;")
        
        self.call_car_button = PacmanButton()
        self.call_car_button.clicked.connect(self.toggle_call_car_button)
        
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.call_car_button, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)
    
    def toggle_call_car_button(self):
        if self.call_car_button.isChecked():
            self.label.setText("Carro chamado para o Box")
            self.call_car_button.setStyleSheet("background-color: red; border-radius: 75px;")
        else:
            self.label.setText("Chamar Carro para o Box")
            self.call_car_button.setStyleSheet("background-color: green; border-radius: 75px;")
