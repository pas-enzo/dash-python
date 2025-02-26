from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont, QFontDatabase
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel
import os

class FourWheelDriveWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ativado = False  # Estado inicial: 4x4 desativado

        # Configurações de tamanho
        self.setMinimumSize(150, 200)  # Aumentei a altura para acomodar a label acima do círculo
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Tamanho fixo

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)  # Espaçamento entre a label e o círculo

        # Label "Acionamento 4x4"
        self.label_titulo = QLabel("Acionamento 4x4")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_titulo)

        # Carregar a fonte "High Speed"
        self.load_high_speed_font()

        # Widget para o círculo
        self.circle_widget = CircleWidget(self)
        layout.addWidget(self.circle_widget)

        # Timer para alternar o estado
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.alternar_estado)
        self.timer.start(2000)  # Alterna a cada 2 segundos

    def load_high_speed_font(self):
        # Carrega a fonte "High Speed"
        font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "High Speed.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                high_speed_font = QFont(font_families[0], 16)  # Tamanho da fonte 16
                self.label_titulo.setFont(high_speed_font)
            else:
                print("Família de fontes não encontrada.")
        else:
            print(f"Fonte 'High Speed.ttf' não carregada. Verifique se o arquivo está no diretório: {font_path}")

    def setAtivado(self, ativado):
        """Define o estado do 4x4 (True para ativado, False para desativado)."""
        if self._ativado != ativado:
            self._ativado = ativado
            self.circle_widget.setAtivado(ativado)  # Atualiza o estado do círculo
            self.circle_widget.update()  # Redesenha o círculo

    def alternar_estado(self):
        """Alterna o estado do 4x4 entre ativado e desativado."""
        self.setAtivado(not self._ativado)

class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ativado = False  # Estado inicial: 4x4 desativado
        self.setMinimumSize(100, 100)  # Tamanho mínimo para o círculo

    def setAtivado(self, ativado):
        """Define o estado do 4x4 (True para ativado, False para desativado)."""
        if self._ativado != ativado:
            self._ativado = ativado
            self.update()  # Redesenha o círculo

    def paintEvent(self, event):
        """Desenha o círculo com a cor correspondente ao estado do 4x4."""
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.Antialiasing)  # Suaviza as bordas do círculo

            # Define a cor do círculo com base no estado do 4x4
            if self._ativado:
                cor = QColor(0, 255, 0)  # Verde para 4x4 ativado
                texto = "acionado"
            else:
                cor = QColor(255, 0, 0)  # Vermelho para 4x4 desativado
                texto = "desacionado"

            # Desenha o círculo
            painter.setBrush(cor)
            painter.setPen(Qt.NoPen)  # Sem borda
            circle_size = min(self.width(), self.height())
            painter.drawEllipse(
                (self.width() - circle_size) // 2,
                (self.height() - circle_size) // 2,
                circle_size,
                circle_size
            )

            # Adiciona um texto indicativo
            painter.setPen(Qt.white)  # Cor do texto
            fonte = painter.font()
            fonte.setPointSize(12)  # Tamanho da fonte
            painter.setFont(fonte)
            painter.drawText(self.rect(), Qt.AlignCenter, texto)  # Ajusta a posição do texto para dentro do círculo