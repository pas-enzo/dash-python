import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor

class MapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Criar um título
        self.title = QLabel("MAPA", self)
        self.title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; text-align: center;")
        self.layout.addWidget(self.title)

        # Criar um widget gráfico
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Configuração visual profissional com fundo preto e bordas azul escuro
        self.plot_widget.setBackground(QColor(0, 0, 0))  # Fundo preto
        self.plot_widget.showGrid(x=True, y=True, alpha=0.1)  # Grid sutil

        # Criar bordas azul escuro mais espessas e detalhadas
        self.plot_widget.setStyleSheet(
            "border-top: 15px solid #193F8B; border-bottom: 15px solid #193F8B; "
            "border-left: 5px solid #0A2A6C; border-right: 5px solid #0A2A6C; "
            "padding: 10px;"
        )
        
        # Remover os eixos para um visual mais limpo
        self.plot_widget.showAxis('left', False)
        self.plot_widget.showAxis('bottom', False)
        
        # Definir escala
        self.plot_widget.setRange(xRange=[-20, 20], yRange=[-20, 20])
        
        # Inicializar trajetória
        self.trajeto_x = []
        self.trajeto_y = []
        self.indice_ponto = 0  # Índice do ponto atual

        # Paleta de cores sem preto
        self.cores_paleta = ['#193F8B', '#078CF2', '#00D3E1', '#1D917D', '#25C99B', '#DFAE21', '#BE9102']
        
        # Criar os pontos da pista com cores variadas
        self.pontos_pista = []
        for i in range(1000):
            cor = self.cores_paleta[i % len(self.cores_paleta)]
            ponto = self.plot_widget.plot([], [], pen=None, symbol='o', symbolBrush=cor, symbolSize=3)
            self.pontos_pista.append(ponto)
        
        # Criar o marcador do carro
        self.marcador_carro = self.plot_widget.plot([], [], pen=None, symbol='o', symbolBrush='#DFAE21', symbolSize=10)  # Cor dourada para o carro

        # Timer para atualizar o movimento do carro
        self.timer = QTimer()
        self.timer.timeout.connect(self.mover_carro)
        self.timer.start(50)  # Atualiza a cada 50ms para suavidade

    def mover_carro(self):
        # Gerar um novo ponto de forma contínua
        novo_x = np.cos(self.indice_ponto / 50) * (10 + np.sin(self.indice_ponto / 20) * 5)
        novo_y = np.sin(self.indice_ponto / 50) * (10 + np.cos(self.indice_ponto / 20) * 5)
        self.trajeto_x.append(novo_x)
        self.trajeto_y.append(novo_y)

        # Remover os primeiros 100 pontos para manter um efeito de trilha
        if len(self.trajeto_x) > 250:
            self.trajeto_x.pop(0)
            self.trajeto_y.pop(0)
        
        # Atualizar os pontos da pista
        for i, ponto in enumerate(self.pontos_pista):
            if i < len(self.trajeto_x):
                ponto.setData([self.trajeto_x[i]], [self.trajeto_y[i]])
            else:
                ponto.setData([], [])
        
        # Atualizar a posição do carro
        self.marcador_carro.setData([novo_x], [novo_y])
        
        self.indice_ponto += 1
