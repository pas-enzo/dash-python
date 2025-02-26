from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget, QSizePolicy
import math

class TacometroWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._valor_atual = 0
        self.direcao = 1
        
        # Configurações de tamanho
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Timer e animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tacometro)
        self.timer.start(50)
        
        self.animation = QPropertyAnimation(self, b"valor_atual")
        self.animation.setDuration(1000)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def update_tacometro(self):
        if self._valor_atual >= 3600:
            self.direcao = -1
        elif self._valor_atual <= 0:
            self.direcao = 1
        self.setValorAtual(self._valor_atual + self.direcao * 50)

    def paintEvent(self, event):
        with QPainter(self) as painter:  # Context manager para gerenciar o painter
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Obter dimensões corretas
            width = self.width()
            height = self.height()
            
            # Centralizar verticalmente
            center_x = width // 2
            center_y = height // 2  # Correção crucial aqui
            
            # Calcular raio proporcional
            radius = min(width, height) // 2 - 20
            
            # Desenhar fundo do semicírculo
            painter.setBrush(QColor(30, 30, 30, 200))
            painter.setPen(Qt.NoPen)
            painter.drawPie(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2,
                180 * 16,
                -180 * 16
            )

            # Desenhar escala
            painter.setPen(QColor(255, 255, 255))
            for i in range(0, 3601, 500):
                angle = math.radians(180 - (i / 3600 * 180))
                
                # Converter coordenadas para inteiros
                x1 = int(center_x + (radius - 10) * math.cos(angle))
                y1 = int(center_y - (radius - 10) * math.sin(angle))
                x2 = int(center_x + (radius - 30) * math.cos(angle))
                y2 = int(center_y - (radius - 30) * math.sin(angle))
                painter.drawLine(x1, y1, x2, y2)
                
                # Texto dos valores
                if i % 1000 == 0:
                    text = str(i)
                    text_width = painter.fontMetrics().horizontalAdvance(text)
                    text_height = painter.fontMetrics().height()
                    
                    x_text = int(center_x + (radius - 50) * math.cos(angle) - text_width/2)
                    y_text = int(center_y - (radius - 50) * math.sin(angle) + text_height/4)
                    painter.drawText(x_text, y_text, text)

            # Desenhar ponteiro
            angle = math.radians(180 - (self._valor_atual / 3600 * 180))
            pointer_length = radius - 50
            
            painter.setPen(QColor(255, 0, 0))
            painter.setBrush(QColor(255, 0, 0, 100))
            
            x_pointer = int(center_x + pointer_length * math.cos(angle))
            y_pointer = int(center_y - pointer_length * math.sin(angle))
            painter.drawLine(center_x, center_y, x_pointer, y_pointer)
            
            # Base do ponteiro
            painter.drawEllipse(center_x - 5, center_y - 5, 10, 10)

    def getValorAtual(self):
        return self._valor_atual

    def setValorAtual(self, value):
        if value != self._valor_atual:
            self._valor_atual = value
            self.update()

    valor_atual = pyqtProperty(float, getValorAtual, setValorAtual)