import sys
import numpy as np
import os
from PyQt5.QtGui import QPixmap, QFont, QIcon, QFontDatabase
from PyQt5.QtWidgets import (
    QAction, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QToolBar, QApplication, QSizePolicy, 
    QToolButton, QLabel, QStackedWidget
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

class RacingDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PacDash 3")
        self.setGeometry(100, 100, 1800, 1000)

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
        layout.setSpacing(5)

        # Criar os quadrantes (widgets vazios)
        quadrantes = [[QWidget() for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                quadrantes[i][j].setObjectName(f"quadrante_{i}_{j}")
                layout.addWidget(quadrantes[i][j], i, j)

        # Garantir que todos os quadrantes tenham o mesmo tamanho
        for i in range(3):
            layout.setRowStretch(i, 1)
            layout.setColumnStretch(i, 1)

        # Criar widgets e adicioná-los nos quadrantes corretos
        velocimetro = VelocimetroWidget()
        barra_combustivel = BarraCombustivelWidget()
        botaobox = CallCarWidget()
        label_info = QLabel("")
        tacometro = TacometroWidget()  # Adiciona o tacômetro

        label_info.setAlignment(Qt.AlignCenter)
        label_info.setStyleSheet("font-size: 18px; color: white;")

        # Criar layouts internos para centralizar os widgets
        layout_velocimetro = QVBoxLayout()
        layout_velocimetro.addWidget(velocimetro)
        layout_velocimetro.setAlignment(Qt.AlignCenter)
        quadrantes[0][1].setLayout(layout_velocimetro)

        layout_combustivel = QVBoxLayout()
        layout_combustivel.addWidget(barra_combustivel)
        layout_combustivel.setAlignment(Qt.AlignCenter)
        quadrantes[2][1].setLayout(layout_combustivel)

        layout_botaobox = QVBoxLayout()
        layout_botaobox.addWidget(botaobox)
        layout_botaobox.setAlignment(Qt.AlignCenter)
        quadrantes[1][2].setLayout(layout_botaobox)

        layout_info = QVBoxLayout()
        layout_info.addWidget(label_info)
        layout_info.setAlignment(Qt.AlignCenter)
        quadrantes[1][1].setLayout(layout_info)

        # Adicionar o tacômetro no canto superior esquerdo (quadrante [0][0])
        layout_tacometro = QVBoxLayout()
        layout_tacometro.addWidget(tacometro)
        layout_tacometro.setAlignment(Qt.AlignCenter)
        quadrantes[0][0].setLayout(layout_tacometro)

        return widget

    def create_car_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        tires_info_label = QLabel("Informações sobre pneus")
        tires_info_label.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(tires_info_label)
        return widget

    def create_graphs_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.dynamic_graphs_widget = pg.GraphicsLayoutWidget(show=True)
        self.dynamic_graphs_widget.setBackground('#2B2B2B')
        layout.addWidget(self.dynamic_graphs_widget)

        self.gforce_plot = self.dynamic_graphs_widget.addPlot(title="Força G (Longitudinal)")
        self.gforce_plot.setLabel('left', 'Força G (g)')
        self.gforce_plot.setLabel('bottom', 'Tempo (s)')
        self.gforce_plot.showGrid(x=True, y=True, alpha=0.3)
        self.gforce_curve = self.gforce_plot.plot(pen=pg.mkPen(color='#FF6347', width=2))

        self.dynamic_graphs_widget.nextRow()

        self.speed_plot = self.dynamic_graphs_widget.addPlot(title="Velocidade")
        self.speed_plot.setLabel('left', 'Velocidade (km/h)')
        self.speed_plot.setLabel('bottom', 'Tempo (s)')
        self.speed_plot.showGrid(x=True, y=True, alpha=0.3)
        self.speed_curve = self.speed_plot.plot(pen=pg.mkPen(color='#00BFFF', width=2))

        self.dynamic_graphs_widget.nextRow()

        self.braking_plot = self.dynamic_graphs_widget.addPlot(title="Temperatura")
        self.braking_plot.setLabel('left', 'Temp (°C)')
        self.braking_plot.setLabel('bottom', 'Tempo (s)')
        self.braking_plot.showGrid(x=True, y=True, alpha=0.3)
        self.braking_curve = self.braking_plot.plot(pen=pg.mkPen(color='#32CD32', width=2))

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dynamic_graphs)
        self.timer.start(1000)

        return widget

    def update_dynamic_graphs(self):
        t = np.linspace(0, 10, 1000)
        gforce = np.sin(t) + np.random.normal(size=1000) * 0.1
        speed = np.abs(np.sin(t / 2)) * 30 + np.random.normal(size=1000) * 5
        braking = np.abs(25 * np.log(t * 19)) + np.random.normal(size=1000) * 0.2

        self.gforce_curve.setData(t, gforce)
        self.speed_curve.setData(t, speed)
        self.braking_curve.setData(t, braking)

    def load_stylesheet(self, path):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(script_dir, path)

            with open(full_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Erro: O arquivo de estilo '{path}' não foi encontrado.")

    def load_fonts(self):
        font_files = ["High Speed.ttf", "High Speed.otf"]
        for font_file in font_files:
            font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), font_file)
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                print(f"Erro ao carregar a fonte: {font_file}")
            else:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"Fonte carregada: {font_file} | Famílias disponíveis: {families}")

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

def main():
    app = QApplication(sys.argv)
    window = RacingDashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()