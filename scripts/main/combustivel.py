from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont, QLinearGradient, QPainterPath
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect


class BarraCombustivelWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._nivel_combustivel = 100  # Nível inicial de combustível
        self.direcao = -1  # Simula a variação do nível
        self.setFixedSize(80, 300)  # Tamanho fixo do widget (mais estreito para parecer profissional)

        # Timer para simular a variação do nível de combustível
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_combustivel)
        self.timer.start(500)  # Atualização a cada 500 ms

        # Adicionar sombra ao widget
        self.setup_shadow()

    def setup_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(3, 3)
        self.setGraphicsEffect(shadow)

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
        bar_width = 40  # Largura da barra
        bar_height = self.height() - 40  # Altura da barra (com margens)
        bar_x = (self.width() - bar_width) // 2  # Centraliza a barra horizontalmente
        bar_y = 20  # Margem superior

        # Fundo da barra (cinza escuro com bordas arredondadas)
        painter.setBrush(QColor(40, 40, 40))
        path = QPainterPath()
        path.addRoundedRect(bar_x, bar_y, bar_width, bar_height, 5, 5)
        painter.drawPath(path)

        # Nível de combustível (com gradiente e bordas arredondadas)
        nivel_height = int((self._nivel_combustivel / 100) * bar_height)
        gradient = QLinearGradient(bar_x, bar_y + bar_height - nivel_height, bar_x, bar_y + bar_height)
        if self._nivel_combustivel > 50:
            gradient.setColorAt(0, QColor(0, 255, 0))  # Verde
            gradient.setColorAt(1, QColor(0, 200, 0))
        elif self._nivel_combustivel > 20:
            gradient.setColorAt(0, QColor(255, 165, 0))  # Laranja
            gradient.setColorAt(1, QColor(200, 120, 0))
        else:
            gradient.setColorAt(0, QColor(255, 0, 0))  # Vermelho
            gradient.setColorAt(1, QColor(200, 0, 0))

        painter.setBrush(gradient)
        nivel_path = QPainterPath()
        nivel_path.addRoundedRect(bar_x, bar_y + bar_height - nivel_height, bar_width, nivel_height, 5, 5)
        painter.drawPath(nivel_path)

        # Marcas de nível (linhas horizontais)
        painter.setPen(QColor(150, 150, 150))
        for i in range(0, 101, 10):  # Marcas de 0% a 100% em intervalos de 10%
            y = bar_y + bar_height - int((i / 100) * bar_height)
            painter.drawLine(bar_x - 5, y, bar_x + bar_width + 5, y)

        # Texto da porcentagem (centralizado na barra)
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.setPen(Qt.white)
        percentage_text = f"{self._nivel_combustivel}%"
        text_width = painter.fontMetrics().horizontalAdvance(percentage_text)
        text_x = bar_x + (bar_width - text_width) // 2
        text_y = bar_y + bar_height + 10  # Posiciona o texto abaixo da barra
        painter.drawText(text_x, text_y, percentage_text)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = BarraCombustivelWidget()
    widget.show()
    sys.exit(app.exec_())