import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class DistanceWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Variável para armazenar a distância percorrida
        self.distance = 0.0  # Em quilômetros

        # Configurações do widget
        self.setWindowTitle("Indicador de Distância Percorrida")
        self.setGeometry(100, 100, 300, 200)

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Rótulo "Distância Percorrida"
        self.label_title = QLabel("Distância Percorrida")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                margin-bottom: 10px;  /* Espaçamento abaixo do título */
            }
        """)
        layout.addWidget(self.label_title)

        # Display da distância percorrida
        self.label_distance = QLabel("0.0 km")
        self.label_distance.setAlignment(Qt.AlignCenter)
        self.label_distance.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: bold;
                color: white;
                background-color: #333333;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        layout.addWidget(self.label_distance)

        # Timer para simular o aumento automático da distância
        self.timer = QTimer()
        self.timer.timeout.connect(self.increase_distance_auto)
        self.timer.start(1000)  # Atualiza a cada 1 segundo

    def increase_distance_auto(self):
        # Aumenta a distância automaticamente em 0.01 km a cada segundo
        self.distance += 0.01
        self.update_display()

    def update_display(self):
        # Atualiza o display com a distância atual
        self.label_distance.setText(f"{self.distance:.2f} km")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DistanceWidget()
    window.show()
    sys.exit(app.exec_())