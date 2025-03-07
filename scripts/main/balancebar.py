import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QLinearGradient


class BrakeBalanceBar(QWidget):
    def __init__(self):
        super().__init__()

        self._front_value = 50  # Valor inicial da força dianteira
        self._rear_value = 50  # Valor inicial da força traseira
        self._dragging = False  # Indica se o usuário está arrastando a linha

        # Configurações do widget
        self.setFixedSize(400, 40)  # Tamanho da barra (mais espessa)
        self.setStyleSheet("""
            background-color: transparent;
        """)

    def update_balance(self, value):
        # Atualiza os valores da força dianteira e traseira
        self._front_value = value
        self._rear_value = 100 - value
        self.update()  # Re-renderiza o widget

    def mousePressEvent(self, event):
        # Inicia o arrasto quando o usuário clica na barra
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self.update_balance_from_mouse(event.pos())

    def mouseMoveEvent(self, event):
        # Atualiza o valor enquanto o usuário arrasta o mouse
        if self._dragging:
            self.update_balance_from_mouse(event.pos())

    def mouseReleaseEvent(self, event):
        # Finaliza o arrasto quando o usuário solta o botão do mouse
        if event.button() == Qt.LeftButton:
            self._dragging = False

    def update_balance_from_mouse(self, pos):
        # Calcula o valor com base na posição do mouse
        value = int((pos.x() / self.width()) * 100)
        value = max(0, min(100, value))  # Limita o valor entre 0 e 100
        self.update_balance(value)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensões da barra
        bar_width = self.width()
        bar_height = 20  # Altura da barra (mais espessa)
        bar_y = (self.height() - bar_height) // 2  # Centraliza verticalmente

        # Fundo da barra (cinza escuro com bordas arredondadas)
        painter.setBrush(QColor(40, 40, 40))
        painter.drawRoundedRect(0, bar_y, bar_width, bar_height, 10, 10)

        # Força dianteira (vermelho com gradiente)
        front_width = int((self._front_value / 100) * bar_width)
        gradient = QLinearGradient(0, bar_y, front_width, bar_y)
        gradient.setColorAt(0, QColor(255, 99, 71))  # Vermelho (dianteira)
        gradient.setColorAt(1, QColor(255, 69, 0))  # Vermelho mais escuro
        painter.setBrush(gradient)
        painter.drawRoundedRect(0, bar_y, front_width, bar_height, 10, 10)

        # Força traseira (azul com gradiente)
        rear_width = int((self._rear_value / 100) * bar_width)
        gradient = QLinearGradient(front_width, bar_y, bar_width, bar_y)
        gradient.setColorAt(0, QColor(30, 144, 255))  # Azul (traseira)
        gradient.setColorAt(1, QColor(0, 0, 205))  # Azul mais escuro
        painter.setBrush(gradient)
        painter.drawRoundedRect(front_width, bar_y, rear_width, bar_height, 10, 10)

        # Texto da porcentagem (centralizado na barra)
        painter.setPen(Qt.white)
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self._front_value}% Dianteira / {self._rear_value}% Traseira")


class BrakeBalanceWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Barra de frenagem personalizada
        self.brake_balance_bar = BrakeBalanceBar()
        layout.addWidget(self.brake_balance_bar)

        # Configurações da janela
        self.setWindowTitle('Balance Bar de Frenagem')
        self.setGeometry(300, 300, 400, 100)
        self.setStyleSheet("""
            QWidget {
                background-color: #2B2B2B;
                color: white;
                font-family: Arial;
                font-size: 12px;
            }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrakeBalanceWidget()
    window.show()
    sys.exit(app.exec_())