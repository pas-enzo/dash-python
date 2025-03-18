import sys
import numpy as np
import os
from PyQt5.QtGui import QPixmap, QFont, QIcon, QFontDatabase, QTransform
from PyQt5.QtWidgets import (
    QAction, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QToolBar, QApplication, QSizePolicy,
    QToolButton, QLabel, QStackedWidget, QFrame
)
from PyQt5.QtCore import Qt, QTimer
import time
import random
from map_view import MapWidget
import pyqtgraph as pg
from velocimetro import VelocimetroWidget
from combustivel import BarraCombustivelWidget
from botaobox import CallCarWidget
from tacometro import TacometroWidget
from acionamento import FourWheelDriveWidget
import logging
import configparser
from balancebar import BrakeBalanceBar
from tmotor import TemperatureMotorWidget
from bateria import BatteryWidget
from distancia import DistanceWidget

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Iniciando a aplicação...")

# Carregar configurações
config = configparser.ConfigParser()
config.read('config.ini')

class TirePressureWidget(QWidget):
    def __init__(self, tire_name, pressure=0.0, parent=None):
        super().__init__(parent)
        self.tire_name = tire_name
        self.pressure = pressure
        self.initUI()

    def initUI(self):
        frame = QFrame(self)
        frame.setStyleSheet("background-color: #303030; padding: 10px; border-radius: 15px;")
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        name_label = QLabel(self.tire_name, self)
        name_label.setFont(QFont("High Speed", 14))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #DFAE21;")

        self.pressure_label = QLabel(f"{self.pressure:.1f} bar", self)
        self.pressure_label.setFont(QFont("High Speed", 16))
        self.pressure_label.setAlignment(Qt.AlignCenter)
        self.pressure_label.setStyleSheet("color: white;")

        layout.addWidget(name_label)
        layout.addWidget(self.pressure_label)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        main_layout.setContentsMargins(0, 0, 0, 0)

    def set_pressure(self, pressure):
        self.pressure = pressure
        self.pressure_label.setText(f"{self.pressure:.1f} bar")

class RacingDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Inicializando RacingDashboard...")
        self.setWindowTitle("PacDash 3")
        self.setGeometry(100, 100, 1800, 1000)

        # Inicializar variáveis dos gráficos antes de criar os widgets
        self.time_window = 10  # Janela de 10 segundos
        self.update_interval = 0.1  # Atualizar a cada 0.1 segundos
        self.time_data = []
        self.gforce_data = []
        self.speed_data = []
        self.braking_data = []
        self.start_time = time.time()

        # Cria o QStackedWidget para gerenciar as diferentes telas
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Carrega as fontes e o estilo
        self.load_fonts()
        self.load_stylesheet("styles.qss")

        # Cria os widgets para cada aba
        self.general_widget = self.create_general_widget()
        self.car_widget = self.create_car_widget()
        self.graphs_widget = self.create_graphs_widget()
        self.map_widget = MapWidget(self)

        # Adiciona os widgets ao QStackedWidget
        self.stacked_widget.addWidget(self.general_widget)
        self.stacked_widget.addWidget(self.car_widget)
        self.stacked_widget.addWidget(self.graphs_widget)
        self.stacked_widget.addWidget(self.map_widget)

        # Inicializa a interface
        self.initUI()

    def create_general_widget(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        font = QFont("High Speed", 16)

        tacometro = TacometroWidget()
        tacometro.setFont(font)
        layout.addWidget(tacometro, 8, 0, 8, 8)

        velocimetro = VelocimetroWidget()
        velocimetro.setFont(font)
        layout.addWidget(velocimetro, 3, 8, 6, 8)

        balancebar = BrakeBalanceBar()
        balancebar.setFont(font)
        layout.addWidget(balancebar, 6, 7, 1, 8)

        barra_combustivel = BarraCombustivelWidget()
        barra_combustivel.setFont(font)
        layout.addWidget(barra_combustivel, 2, 0, 1, 3)

        Temperaturamotor = TemperatureMotorWidget()
        Temperaturamotor.setFont(font)
        layout.addWidget(Temperaturamotor, 1, 11, 3, 4)

        four_wheel_drive = FourWheelDriveWidget()
        four_wheel_drive.setFont(font)
        layout.addWidget(four_wheel_drive, 2, 2, 2, 4)

        botaobox = CallCarWidget()
        botaobox.setFont(font)
        layout.addWidget(botaobox, 4, 12, 3, 6)

        bateria = BatteryWidget()
        bateria.setFont(font)
        layout.addWidget(bateria, 4, 2, 3, 5)

        distancia = DistanceWidget()
        distancia.setFont(font)
        layout.addWidget(distancia, 2, 7, 2, 3)

        for row in range(10):
            layout.setRowStretch(row, 1)
        for col in range(20):
            layout.setColumnStretch(col, 1)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 2)
        layout.setRowStretch(5, 2)
        layout.setRowStretch(6, 2)
        layout.setRowStretch(7, 2)
        layout.setRowStretch(8, 1)
        layout.setRowStretch(9, 1)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(7, 2)
        layout.setColumnStretch(8, 2)
        layout.setColumnStretch(15, 2)
        layout.setColumnStretch(16, 1)
        layout.setColumnStretch(19, 1)

        return widget

    def create_car_widget(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)

        container = QFrame(widget)
        container.setStyleSheet("background-color: #303030; padding: 20px; border-radius: 20px;")
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignCenter)

        car_label = QLabel(container)
        car_label.setAlignment(Qt.AlignCenter)
        car_label.setFont(QFont("High Speed", 16))

        script_dir = os.path.dirname(os.path.abspath(__file__))
        car_image_path = os.path.join(script_dir, "teleeeeeeeeeeeeeemetria_porraaaaaa.png")

        if os.path.exists(car_image_path):
            pixmap = QPixmap(car_image_path)
            scaled_pixmap = pixmap.scaled(
                int(pixmap.width() * 1.5),
                int(pixmap.height() * 1.5),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            transform = QTransform()
            transform.rotate(-90)
            rotated_pixmap = scaled_pixmap.transformed(transform, Qt.SmoothTransformation)
            car_label.setPixmap(rotated_pixmap)
        else:
            logger.error(f"Erro: A imagem do carro '{car_image_path}' não foi encontrada.")

        container_layout.addWidget(car_label)

        front_left = TirePressureWidget("Frente Esquerda", 2.5)
        front_right = TirePressureWidget("Frente Direita", 2.5)
        rear_left = TirePressureWidget("Traseira Esquerda", 2.4)
        rear_right = TirePressureWidget("Traseira Direita", 2.4)

        layout.addWidget(front_left, 0, 0, 1, 1)
        layout.addWidget(front_right, 0, 2, 1, 1)
        layout.addWidget(container, 0, 1, 3, 1)
        layout.addWidget(rear_left, 2, 0, 1, 1)
        layout.addWidget(rear_right, 2, 2, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)

        return widget

    def create_graphs_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.dynamic_graphs_widget = pg.GraphicsLayoutWidget(show=True)
        self.dynamic_graphs_widget.setBackground('#2B2B2B')
        layout.addWidget(self.dynamic_graphs_widget)

        font = QFont("High Speed", 12)

        # Força G
        self.gforce_plot = self.dynamic_graphs_widget.addPlot(title="Força G (Longitudinal)")
        self.gforce_plot.setLabel('left', 'Força G (g)')
        self.gforce_plot.setLabel('bottom', 'Tempo (s)')
        self.gforce_plot.showGrid(x=True, y=True, alpha=0.3)
        self.gforce_plot.getAxis('left').setFont(font)
        self.gforce_plot.getAxis('bottom').setFont(font)
        self.gforce_plot.titleLabel.item.setFont(font)
        self.gforce_curve = self.gforce_plot.plot(pen=pg.mkPen(color='#FF6347', width=2))
        self.gforce_plot.setRange(xRange=[0, self.time_window], yRange=[-2, 2])  # Limites iniciais

        self.dynamic_graphs_widget.nextRow()

        # Velocidade
        self.speed_plot = self.dynamic_graphs_widget.addPlot(title="Velocidade")
        self.speed_plot.setLabel('left', 'Velocidade (km/h)')
        self.speed_plot.setLabel('bottom', 'Tempo (s)')
        self.speed_plot.showGrid(x=True, y=True, alpha=0.3)
        self.speed_plot.getAxis('left').setFont(font)
        self.speed_plot.getAxis('bottom').setFont(font)
        self.speed_plot.titleLabel.item.setFont(font)
        self.speed_curve = self.speed_plot.plot(pen=pg.mkPen(color='#00BFFF', width=2))
        self.speed_plot.setRange(xRange=[0, self.time_window], yRange=[0, 50])  # Limites iniciais

        self.dynamic_graphs_widget.nextRow()

        # Temperatura
        self.braking_plot = self.dynamic_graphs_widget.addPlot(title="Temperatura")
        self.braking_plot.setLabel('left', 'Temp (°C)')
        self.braking_plot.setLabel('bottom', 'Tempo (s)')
        self.braking_plot.showGrid(x=True, y=True, alpha=0.3)
        self.braking_plot.getAxis('left').setFont(font)
        self.braking_plot.getAxis('bottom').setFont(font)
        self.braking_plot.titleLabel.item.setFont(font)
        self.braking_curve = self.braking_plot.plot(pen=pg.mkPen(color='#32CD32', width=2))
        self.braking_plot.setRange(xRange=[0, self.time_window], yRange=[0, 100])  # Limites iniciais

        # Configurar o timer para atualização rápida
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dynamic_graphs)
        self.timer.start(int(self.update_interval * 1000))  # Atualizar a cada 100ms

        return widget

    def update_dynamic_graphs(self):
        try:
            # Tempo atual relativo ao início
            current_time = time.time() - self.start_time

            # Gerar novos dados simulados
            gforce = np.sin(current_time) + random.normalvariate(0, 0.1)
            speed = abs(np.sin(current_time / 2)) * 30 + random.normalvariate(0, 5)
            braking = abs(25 * np.log(current_time + 1)) + random.normalvariate(0, 0.2)

            # Adicionar novos dados
            self.time_data.append(current_time)
            self.gforce_data.append(gforce)
            self.speed_data.append(speed)
            self.braking_data.append(braking)

            # Manter apenas os dados dentro da janela de tempo
            while self.time_data and self.time_data[0] < current_time - self.time_window:
                self.time_data.pop(0)
                self.gforce_data.pop(0)
                self.speed_data.pop(0)
                self.braking_data.pop(0)

            # Converter para arrays NumPy para plotagem
            time_array = np.array(self.time_data)
            gforce_array = np.array(self.gforce_data)
            speed_array = np.array(self.speed_data)
            braking_array = np.array(self.braking_data)

            # Ajustar o eixo X para deslizar
            if len(time_array) > 1:
                x_min = max(0, current_time - self.time_window)
                x_max = current_time
                self.gforce_plot.setRange(xRange=[x_min, x_max])
                self.speed_plot.setRange(xRange=[x_min, x_max])
                self.braking_plot.setRange(xRange=[x_min, x_max])

            # Atualizar os gráficos
            self.gforce_curve.setData(time_array, gforce_array)
            self.speed_curve.setData(time_array, speed_array)
            self.braking_curve.setData(time_array, braking_array)

        except Exception as e:
            logger.error(f"Erro ao atualizar gráficos: {e}")

    def load_stylesheet(self, path):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(script_dir, path)
            with open(full_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            logger.error(f"Erro: O arquivo de estilo '{path}' não foi encontrado.")
        except Exception as e:
            logger.error(f"Erro ao carregar o arquivo de estilo: {e}")

    def load_fonts(self):
        font_files = ["High Speed.ttf", "High Speed.otf"]
        for font_file in font_files:
            try:
                font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id == -1:
                    logger.error(f"Erro ao carregar a fonte: {font_file}")
                else:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    logger.info(f"Fonte carregada: {font_file} | Famílias disponíveis: {families}")
            except Exception as e:
                logger.error(f"Erro ao carregar a fonte {font_file}: {e}")

    def initUI(self):
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbar.setMovable(False)
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        actions = [
            QAction(QIcon(), "Geral", self),
            QAction(QIcon(), "Carro", self),
            QAction(QIcon(), "Gráficos", self),
            QAction(QIcon(), "Mapa", self),
        ]

        for action in actions:
            button = QToolButton(self)
            button.setText(action.text())
            button.setIcon(action.icon())
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            toolbar.addWidget(button)
            button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        button = self.sender()
        button_name = button.text()

        if button_name == "Geral":
            self.stacked_widget.setCurrentWidget(self.general_widget)
        elif button_name == "Carro":
            self.stacked_widget.setCurrentWidget(self.car_widget)
        elif button_name == "Gráficos":
            self.stacked_widget.setCurrentWidget(self.graphs_widget)
        elif button_name == "Mapa":
            self.stacked_widget.setCurrentWidget(self.map_widget)

    def resizeEvent(self, event):
        if hasattr(self, 'background_label') and self.background_label.pixmap():
            pixmap = self.background_label.pixmap()
            scaled_pixmap = pixmap.scaled(
                self.background_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.background_label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = RacingDashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()