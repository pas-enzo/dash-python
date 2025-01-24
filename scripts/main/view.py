import sys
import numpy as np
import os
from PyQt5.QtGui import QPixmap, QFont, QIcon, QFontDatabase
from PyQt5.QtWidgets import (
    QAction, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QToolBar, QApplication, QSizePolicy, QToolButton, QLabel
)
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
from velocimetro import VelocimetroWidget
from combustivel import BarraCombustivelWidget

class RacingDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PacDash 3")
        self.setGeometry(100, 100, 1800, 1000)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QGridLayout(self.main_widget)
        self.main_widget.setLayout(self.layout)
        
        self.load_fonts()

        # Carregar a folha de estilo
        self.load_stylesheet("styles.qss")
        self.initUI()

    def load_stylesheet(self, path):
        """Carrega a folha de estilo externa."""
        try:
            # Obtém o diretório atual do script e cria o caminho absoluto para o arquivo .qss
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(script_dir, path)

            with open(full_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Erro: O arquivo de estilo '{path}' não foi encontrado.")
            
    def load_fonts(self):
        """Carrega fontes personalizadas da pasta local."""
        font_files = ["High Speed.ttf", "High Speed.otf"]  # Substitua pelos nomes das suas fontes
        for font_file in font_files:
            font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), font_file)
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                print(f"Erro ao carregar a fonte: {font_file}")
            else:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"Fonte carregada: {font_file} | Famílias disponíveis: {families}")

    def initUI(self):
        # Add a toolbar
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbar.setMovable(False)
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add actions to the toolbar with spacers
        actions = [
            QAction(QIcon(), "Geral", self),
            QAction(QIcon(), "Pneus", self),
            QAction(QIcon(), "Gráficos", self),
            QAction(QIcon(), "Mapa", self),
        ]

        for action in actions:
            button = QToolButton(self)
            button.setText(action.text())
            button.setIcon(action.icon())
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Expanding to fill space
            toolbar.addWidget(button)
            # Conectar o evento de clique
            button.clicked.connect(self.on_button_click)

        # Adicionando widgets específicos ao layout
        self.add_widgets()
        self.plot_dynamic_graphs()

    def on_button_click(self):
        """Método chamado quando um botão da toolbar é clicado."""
        button = self.sender()  # Obtém o botão que foi clicado
        button_name = button.text()
        # print(f"Botão '{button_name}' foi clicado!")

        # Aqui você pode adicionar lógica para o que deve acontecer
        # quando cada botão for clicado, como mudar o conteúdo da interface, etc.
        if button_name == "Geral":
            self.show_general_info()
        elif button_name == "Pneus":
            self.show_tires_info()
        elif button_name == "Gráficos":
            self.show_graphs()
        elif button_name == "Mapa":
            self.show_map()
            
    def clear_screen(self):
        """Limpa todos os widgets do layout principal, mas não a QToolBar."""
        for i in reversed(range(self.layout.count())):
            widget_item = self.layout.itemAt(i)
            if widget_item.widget() is not None:
                widget_item.widget().deleteLater()

    def show_general_info(self):
        self.clear_screen()
        print("Exibindo informações gerais...")
        
        # Exemplo de como adicionar um novo widget (por exemplo, um QLabel)
        general_info_label = QLabel("Informações gerais do sistema")
        self.layout.addWidget(general_info_label, 0, 0)

    def show_tires_info(self):
        self.clear_screen()
        print("Exibindo informações sobre pneus...")
        
        # Exemplo de como adicionar um novo widget (por exemplo, um gráfico ou outro componente)
        tires_info_label = QLabel("Informações sobre pneus")
        self.layout.addWidget(tires_info_label, 0, 0)

    def show_graphs(self):
        self.clear_screen()
        print("Exibindo gráficos...")
        
        # Exemplo de como adicionar um gráfico
        self.plot_dynamic_graphs()

    def show_map(self):
        self.clear_screen()
        print("Exibindo mapa...")
        
        # Exemplo de como adicionar um mapa (ou outro widget)
        map_widget = QLabel("Mapa do circuito")
        self.layout.addWidget(map_widget, 0, 0)

        
    def add_widgets(self):
        # Adicionando o velocímetro
        self.velocimetro = VelocimetroWidget()
        self.layout.addWidget(self.velocimetro, 0, 0, 2, 1)  # Ocupa 2 linhas e 1 coluna

        # Adicionando a barra de combustível
        self.barra_combustivel = BarraCombustivelWidget()
        self.layout.addWidget(self.barra_combustivel, 0, 3, 2, 1)  # Ocupa 2 linhas e 1 coluna

        # Layout para gráficos dinâmicos
        self.dynamic_graphs_widget = pg.GraphicsLayoutWidget(show=True)
        self.dynamic_graphs_widget.setBackground('#2B2B2B')
        self.layout.addWidget(self.dynamic_graphs_widget, 2, 0, 4, 4)  # Ocupa 4 linhas e 4 colunas

    def plot_dynamic_graphs(self):
        # Example graphs for different metrics
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

    def update_dynamic_graphs(self):
        # Simulated dynamic data
        t = np.linspace(0, 10, 1000)
        gforce = np.sin(t) + np.random.normal(size=1000) * 0.1
        speed = np.abs(np.sin(t / 2)) * 30 + np.random.normal(size=1000) * 5
        braking = np.abs(25 * np.log(t * 19)) + np.random.normal(size=1000) * 0.2

        self.gforce_curve.setData(t, gforce)
        self.speed_curve.setData(t, speed)
        self.braking_curve.setData(t, braking)

def main():
    app = QApplication(sys.argv)
    window = RacingDashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
