import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor


class TemperatureMotorWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Variável para armazenar a temperatura do motor
        self.temperature = 50.0  # Valor inicial da temperatura em °C

        # Configurações do widget
        self.setWindowTitle("Indicador de Temperatura do Motor")
        self.setGeometry(100, 100, 300, 200)

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Rótulo "Temperatura do Motor"
        self.label_title = QLabel("Temperatura do Motor")
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

        # Display da temperatura do motor
        self.label_temperature = QLabel("50.0 °C")
        self.label_temperature.setAlignment(Qt.AlignCenter)
        self.label_temperature.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: bold;
                color: white;
                background-color: #333333;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        layout.addWidget(self.label_temperature)

        # Timer para simular a variação automática da temperatura
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temperature_auto)
        self.timer.start(1000)  # Atualiza a cada 1 segundo

    def update_temperature_auto(self):
        # Simula a variação da temperatura do motor
        if self.temperature < 90.0:  # Aumenta a temperatura até 90°C
            self.temperature += 0.5
        else:
            self.temperature = 50.0  # Reseta para 50°C após atingir 90°C

        # Atualiza o display com a temperatura atual
        self.update_display()

    def update_display(self):
        # Atualiza o display com a temperatura atual
        self.label_temperature.setText(f"{self.temperature:.1f} °C")

        # Muda a cor do texto com base na temperatura
        if self.temperature < 70.0:
            color = QColor(0, 255, 0)  # Verde (temperatura segura)
        elif 70.0 <= self.temperature < 85.0:
            color = QColor(255, 255, 0)  # Amarelo (alerta)
        else:
            color = QColor(255, 0, 0)  # Vermelho (perigo)

        # Aplica a cor ao texto
        self.label_temperature.setStyleSheet(f"""
            QLabel {{
                font-size: 40px;
                font-weight: bold;
                color: {color.name()};
                background-color: #333333;
                border-radius: 10px;
                padding: 20px;
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperatureWidget()
    window.show()
    sys.exit(app.exec_())