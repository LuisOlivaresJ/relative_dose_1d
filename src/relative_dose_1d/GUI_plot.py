# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
import numpy as np
from tools import gamma_1D
import sys

class Q_Figure_Block:
        
    def __init__(self):
        self.fig = Figure(figsize=(4,3), tight_layout = True, facecolor = 'whitesmoke')
        self.Qt_fig = FigureCanvas(self.fig)

        #   Axes para la imagen
        self.ax_perfil = self.fig.add_subplot(1, 2, 1)
        self.ax_perfil.set_ylabel('Percentage [%]')
        self.ax_perfil.set_xlabel('Distance')
        self.ax_perfil.grid(alpha = 0.3)

        self.ax_perfil_resta =  self.fig.add_subplot(1, 2, 2)
        self.ax_perfil_resta.set_ylabel('Percentage [%]')
        self.ax_perfil_resta.set_xlabel('Distance [mm]')
        self.ax_perfil_resta.grid(alpha = 0.3)

        self.ax_gamma = self.ax_perfil_resta.twinx()
        self.ax_gamma.set_ylabel('gamma')
        #self.ax_gamma.set_ylim((0, 2))
        
    def plot_data(self, data):
        x = data[:,0]
        y = data[:,1]
        self.ax_perfil.plot(x, y)
        self.ax_perfil.set_ylabel('Percentage [%]')
        self.ax_perfil.set_xlabel('Distance [mm]')
        self.ax_perfil.grid(alpha = 0.3)
        self.fig.canvas.draw()
        
    def plot_resta(self, data):
        x = data[:,0]
        y = data[:,1]
        self.ax_perfil_resta.plot(x, y, color='r', label = 'Diferencia', alpha = 0.6)
        self.ax_perfil_resta.set_ylabel('Diferencia')
        self.ax_perfil_resta.set_xlabel('Distance [mm]')
        self.ax_perfil_resta.grid(alpha = 0.3)
        self.ax_perfil_resta.legend(loc = 'upper left')

        self.fig.canvas.draw()

    def plot_gamma(self, data):
        x = data[:,0]
        y = data[:,1]

        self.ax_gamma.plot(x, y, color='g', label = 'gamma', marker = '.')
        self.ax_gamma.set_ylabel('gamma')
        self.ax_gamma.legend(loc = 'upper right')

        self.fig.canvas.draw()

def plot_profiles_and_results(
        P_ref, 
        P_eval,
        dose_t = 3,
        q=1
        ):
    """"
    A function to make a new window to show the given profiles, gamma and difference comparison.
    
    Parameters
    ----------

    P_ref : ndarray,
        A numpy array with shape (M,2), representing a reference profile. 
        The first column satates the profile positions.

    P_eval : ndarray,
        A numpy array with shape (M,2), representing the evaluated profile. 
        The first column satates the profile positions.

    Returns
    -------

    GUI Window, PyQt
        A new GUI window showing the profiles, gamma and difference comparison.
        
    Examples
    --------

    >>> from tools import build_from_array_and_step

    >>> a = np.array([2,4,6,8,10])
    >>> b = a + np.random.random_sample((5,))
    >>> A = build_from_array_and_step(a, 0.5)
    >>> B = build_from_array_and_step(b, 0.5)

    >>> plot_profiles_and_results(A,B)
    
    """

    class Window(QWidget):

        def __init__(self):
            """Constructor for Empty Window Class"""
            super().__init__()
            self.initializeUI()

        def initializeUI(self):
            """Set up the apllication"""
            "x, y, width, height"
            self.setGeometry(200,100,1000,400)
            self.setWindowTitle("Relative dose 1D")

            self.set_up()
            self.show()

        def set_up(self):
            self.main_box_layout = QVBoxLayout()
            self.setLayout(self.main_box_layout)
            self.Q_grafica = Q_Figure_Block() 
            self.main_box_layout.addWidget(self.Q_grafica.Qt_fig)

            data_A = P_ref
            data_B = P_eval

            # New values ​​of B are computed at positions given by A, using interpolation.
            data_B_from_A_positions = np.interp(data_A[:,0], data_B[:,0], data_B[:,1], left = np.nan)
        
            difference = data_A[:,1] - data_B_from_A_positions

            added_positions = np.array((data_A[:,0], difference))
            values = np.transpose(added_positions)
        
            g, g_percent = gamma_1D(data_A, data_B)

            self.Q_grafica.plot_data(P_ref)
            self.Q_grafica.plot_data(P_eval)
            self.Q_grafica.plot_resta(values)
            self.Q_grafica.plot_gamma(g)
    
    app = QApplication(sys.argv)
    window = Window()

    def plot_data(Profile):
        window.Q_grafica.plot_data(Profile)
    
    #def plot_gamma
    
    def show():
        sys.exit(app.exec())

if __name__ == '__main__':

    from tools import build_from_array_and_step

    a = np.array([2,4,6,8,10])
    b = a + np.random.random_sample((5,))
    A = build_from_array_and_step(a, 0.5)
    B = build_from_array_and_step(b, 0.5)

    plot_profiles_and_results(A,B)
    