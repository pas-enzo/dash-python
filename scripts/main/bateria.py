import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen

class BatteryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bateria")
        self.setGeometry(100, 100, 400, 150)
        self.battery_level = 100  # Começa cheia
        self.decreasing = True  # Flag para controle do aumento/diminuição
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_battery_level)
        self.timer.start(200)  # Atualiza a cada 200ms

    def update_battery_level(self):
        if self.decreasing:
            self.battery_level -= 2
            if self.battery_level <= 0:
                self.battery_level = 0
                self.decreasing = False
        else:
            self.battery_level += 2
            if self.battery_level >= 100:
                self.battery_level = 100
                self.decreasing = True
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)
        
        # Desenha a estrutura da bateria
        painter.drawRect(100, 50, 200, 80)  # Corpo principal
        painter.drawRect(300, 75, 20, 30)  # Terminal direito
        
        # Define o nível da carga dentro da bateria
        fill_width = int((self.battery_level / 100) * 180)  # Calcula a largura da carga
        painter.setBrush(Qt.black)
        painter.drawRect(110, 60, fill_width, 60)  # Barras internas da bateria

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BatteryWidget()
    window.show()
    sys.exit(app.exec_())