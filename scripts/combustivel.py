from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget


class BarraCombustivelWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._nivel_combustivel = 100  # Nível inicial de combustível
        self.direcao = -1  # Simula a variação do nível
        self.setFixedSize(200, 400)
        self.setStyleSheet("background-color: transparent;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_combustivel)
        self.timer.start(500)  # Atualização a cada 500 ms

    def update_combustivel(self):
        # Atualiza o nível de combustível
        if self._nivel_combustivel <= 0:
            self.direcao = 1
        elif self._nivel_combustivel >= 100:
            self.direcao = -1
        self._nivel_combustivel += self.direcao * 5
        self.update()  # Re-renderiza o widget

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensões da barra
        bar_x = self.width() // 4
        bar_width = self.width() // 2
        bar_height = self.height()
        nivel_height = int((self._nivel_combustivel / 100) * bar_height)

        # Fundo da barra
        painter.setBrush(QColor(50, 50, 50))
        painter.drawRect(bar_x, 0, bar_width, bar_height)

        # Nível de combustível
        if self._nivel_combustivel > 50:
            color = QColor(34, 139, 34)  # Verde
        elif self._nivel_combustivel > 20:
            color = QColor(255, 165, 0)  # Laranja
        else:
            color = QColor(255, 0, 0)  # Vermelho
        painter.setBrush(color)
        painter.drawRect(bar_x, bar_height - nivel_height, bar_width, nivel_height)

        # Adicionando a porcentagem ao lado
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        percentage_text = f"{self._nivel_combustivel}%"
        text_x = bar_x + bar_width + 10
        text_y = bar_height - nivel_height - 10
        painter.setPen(Qt.white)
        painter.drawText(text_x, text_y, percentage_text)
