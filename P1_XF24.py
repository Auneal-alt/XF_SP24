import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Model:
    def __init__(self):
        self.gc = 32.2  # gravity constant in lbm*ft/(lbf*s^2)
        self.C_Lmax = 2.4
        self.C_D = 0.0279
        self.rho = 0.002377  # Air density in slugs/ft^3

    def v_stall(self, weight, S):
        return ((2 * weight) / (self.rho * S * self.C_Lmax))**0.5

    def calculate_sto(self, weight, thrust, S):
        V_stall = self.v_stall(weight, S)
        V_TO = 1.2 * V_stall
        A = (thrust / weight) * self.gc
        B = (self.gc / (2 * weight)) * self.rho * S * self.C_D

        v_values = np.linspace(0, V_TO, 500)
        dv = v_values[1] - v_values[0]
        integrand = 1 / (A - B * v_values**2)
        sto = np.sum(integrand) * dv
        return sto


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(PlotCanvas, self).__init__(fig)
        self.setParent(parent)

    def plot(self, thrust, weights, S):
        self.ax.clear()
        thrust_range = np.linspace(1000, 30000, 100)
        for weight in weights:
            sto_data = [model.calculate_sto(weight, t, S) for t in thrust_range]
            self.ax.plot(thrust_range, sto_data, label=f'Weight {weight} lb')

            # Find the STO value at the specified thrust for each weight
            specific_sto = model.calculate_sto(weight, thrust, S)
            self.ax.scatter(thrust, specific_sto, color='red', s=50, zorder=5)  # plot the point as a red circle

        self.ax.set_title('Take-off Distance vs. Engine Thrust')
        self.ax.set_xlabel('Engine Thrust (lbf)')
        self.ax.set_ylabel('STO (ft)')
        self.ax.legend()
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Take-off Distance Calculator")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.weightEdit = QLineEdit(self)
        self.weightEdit.setPlaceholderText("Enter the aircraft weight in lb")
        layout.addWidget(self.weightEdit)

        self.thrustEdit = QLineEdit(self)
        self.thrustEdit.setPlaceholderText("Enter the engine thrust in lbf")
        layout.addWidget(self.thrustEdit)

        self.areaEdit = QLineEdit(self)
        self.areaEdit.setPlaceholderText("Enter the wing area in sq ft")
        layout.addWidget(self.areaEdit)

        self.calcButton = QPushButton('Calculate', self)
        self.calcButton.clicked.connect(self.onCalc)
        layout.addWidget(self.calcButton)

        self.canvas = PlotCanvas(self, width=8, height=6)
        layout.addWidget(self.canvas)

        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def onCalc(self):
        weight = float(self.weightEdit.text())
        thrust = float(self.thrustEdit.text())
        S = float(self.areaEdit.text())
        weights = [weight - 10000, weight, weight + 10000]
        self.canvas.plot(thrust, weights, S)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    main = MainWindow(model)
    main.show()
    sys.exit(app.exec_())
