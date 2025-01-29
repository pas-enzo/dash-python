from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget
import math

class TacometroWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._valor_atual = 0  # Valor inicial
        self.direcao = 1  # Direção: 1 para subir, -1 para descer

        # Timer para atualizar o tacômetro
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tacometro)
        self.timer.start(100)  # Atualizações a cada 100 ms

        # Animação para o ponteiro
        self.animation = QPropertyAnimation(self, b"valor_atual")
        self.animation.setDuration(500)  # Duração da animação
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # Curva de suavização

    def update_tacometro(self):
        # Simulação do tacômetro indo de 0 a 3600 e depois voltando de 3600 a 0
        if self._valor_atual >= 3600:
            self.direcao = -1
        elif self._valor_atual <= 0:
            self.direcao = 1

        nova_velocidade = self._valor_atual + self.direcao * 10  # Ajustando a velocidade de variação
        self.setVelocidade(nova_velocidade)

    def setVelocidade(self, valor):
        self._valor_atual = valor
        self.update()  # Força a atualização

    def paintEvent(self, event):
        # Criação do objeto QPainter para desenhar o tacômetro
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calcula dinamicamente o centro e o raio
        center_x = self.width() // 2
        center_y = self.height() // 2  # Ajuste para alinhar o meio-círculo na parte superior
        radius = min(self.width(), self.height() * 2) // 3  # Proporção ajustada

        # Desenhando o fundo transparente
        painter.setBrush(Qt.NoBrush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())

        # Configurações do meio círculo
        painter.setPen(QColor(255, 255, 255))

        # Desenhando a escala
        for i in range(0, 3601, 500):  # Escala de 0 a 3600
            angle = math.radians(180 - (180 * (i / 3600)))  # Ajuste para direção correta
            x1 = int(center_x + radius * math.cos(angle))
            y1 = int(center_y - radius * math.sin(angle))
            x2 = int(center_x + (radius - 20) * math.cos(angle))
            y2 = int(center_y - (radius - 20) * math.sin(angle))
            painter.drawLine(x1, y1, x2, y2)

        # Desenhando os números na ordem correta
        painter.setFont(QFont("Arial", 10))
        for i in range(0, 3601, 500):  # Mostra todos os valores (incluindo intermediários)
            angle = math.radians(180 - (180 * (i / 3600)))  # Ajuste para direção correta
            x = int(center_x + (radius - 40) * math.cos(angle))
            y = int(center_y - (radius - 40) * math.sin(angle))

            text = str(i)  # Números em ordem crescente
            text_width = painter.fontMetrics().horizontalAdvance(text)
            text_height = painter.fontMetrics().height()
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(x - text_width // 2, y + text_height // 4, text)

        # Desenhando o ponteiro a partir do lado esquerdo
        angle = math.radians(180 - (180 * (self._valor_atual / 3600)))  # Ajuste para direção correta
        x1 = int(center_x + (radius - 60) * math.cos(angle))
        y1 = int(center_y - (radius - 60) * math.sin(angle))
        painter.setPen(QColor(255, 0, 0))
        painter.drawLine(center_x, center_y, x1, y1)

        painter.end()

    def getValorAtual(self):
        return self._valor_atual

    def setValorAtual(self, value):
        if value != self._valor_atual:  # Evita loops desnecessários
            self._valor_atual = value
            self.update()  # Força a atualização

    valor_atual = pyqtProperty(float, getValorAtual, setValorAtual)
