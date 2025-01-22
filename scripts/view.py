import sys
import numpy as np
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg

class RacingDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PacDash 3")
        self.setGeometry(100, 100, 1800, 1000)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QGridLayout(self.main_widget)
        self.main_widget.setLayout(self.layout)

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #2B2B2B; color: white;")

        # Add a toolbar
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(toolbar)
        toolbar.setStyleSheet("background-color: #2B2B2B; color: white;")

        # Add actions to the toolbar
        general_action = QAction(QIcon(), "Geral", self)
        RPM_action = QAction(QIcon(), "RPM", self)
        speed_action = QAction(QIcon(), "Velocidade", self)
        angle_action = QAction(QIcon(), "Ângulo", self)
        lat_gforce_action = QAction(QIcon(), "G-Lateral", self)
        long_gforce_action = QAction(QIcon(), "G-Longitudinal", self)
        temp_action = QAction(QIcon(), "Temperatura CVT", self)

        toolbar.addAction(general_action)
        toolbar.addAction(RPM_action)
        toolbar.addAction(speed_action)
        toolbar.addAction(angle_action)
        toolbar.addAction(lat_gforce_action)
        toolbar.addAction(long_gforce_action)
        toolbar.addAction(temp_action)

        toolbar_layout = QHBoxLayout()
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_layout.addWidget(toolbar)
        toolbar_layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(toolbar_widget, 0, 0, 1, 4)

        central_layout = QVBoxLayout()
        self.dynamic_graphs_widget = pg.GraphicsLayoutWidget(show=True)
        self.dynamic_graphs_widget.setBackground('#2B2B2B')
        central_layout.addWidget(self.dynamic_graphs_widget)

        self.layout.addLayout(central_layout, 1, 1, 1, 2)
        self.plot_dynamic_graphs()

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
