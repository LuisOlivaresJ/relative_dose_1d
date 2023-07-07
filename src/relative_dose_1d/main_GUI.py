# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout,
                             QPushButton, QMessageBox, QFileDialog, QVBoxLayout,
                             QFormLayout, QInputDialog, QMainWindow)
from PyQt6.QtCore import Qt
import numpy as np
from relative_dose_1d.tools import identify_format, get_data, gamma_1D
import sys
import os

class Main_Window(QWidget):

    def __init__(self):
        """Constructor for Empty Window Class"""
        super().__init__()
        self.loaded_data = []
        self.initializeUI()

    def initializeUI(self):
        """Set up the apllication"""
        "x, y, width, height"
        self.setGeometry(200,100,1000,400)
        self.setWindowTitle("Relative dose 1D")

        self.set_up()
        self.show()

    def set_up(self):
        "Layouts definition"
        self.main_box_layout = QHBoxLayout()
   
        self.v_box_layout = QVBoxLayout()
        self.settings_layout_v = QVBoxLayout()
        
        self.Q_grafica = Q_Base_Figure() 


        self.main_box_layout.addLayout(self.settings_layout_v)
        self.main_box_layout.addLayout(self.v_box_layout)

        self.setLayout(self.main_box_layout)

        self.open_file_button = QPushButton("Load a text file", self)
        self.open_file_button.clicked.connect(self.open_file_button_clicked)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_data_and_plots)
        
        self.button_factor = QPushButton("Scale factor", self)
        self.button_factor.clicked.connect(self.factor_button_clicked)
        self.button_factor.setFixedSize(80, 40)
        self.button_factor.setEnabled(False)

        self.button_origin = QPushButton("Move origin", self)
        self.button_origin.clicked.connect(self.move_button_clicked)
        self.button_origin.setFixedSize(80, 40)
        self.button_origin.setEnabled(False)

        self.settings_layout_v.addWidget(QLabel("Axis position", alignment = Qt.AlignmentFlag.AlignHCenter))
        self.settings_layout_v.addWidget(self.button_factor)
        self.settings_layout_v.addWidget(self.button_origin)
        self.settings_layout_v.addWidget(QLabel("Gamma", alignment = Qt.AlignmentFlag.AlignHCenter))

        gammaLayout = QFormLayout()
        self.dose_t_QLine = QLineEdit()
        self.dose_t_QLine.setFixedWidth(40)
        self.dose_t_QLine.setText("3.0")
        self.DTA_t_QLine = QLineEdit()
        self.DTA_t_QLine.setFixedWidth(40)
        self.DTA_t_QLine.setText("2.0")
        self.thres_QLine = QLineEdit()
        self.thres_QLine.setFixedWidth(40)
        self.thres_QLine.setText("0.0")
        self.interp_QLine = QLineEdit()
        self.interp_QLine.setFixedWidth(40)
        self.interp_QLine.setText("1")
        gammaLayout.addRow("Dose [%]:", self.dose_t_QLine)
        gammaLayout.addRow("DTA [mm]:", self.DTA_t_QLine)
        gammaLayout.addRow("Threshold [%]:", self.thres_QLine)
        gammaLayout.addRow("Interp.:", self.interp_QLine)

        self.settings_layout_v.addLayout(gammaLayout)

        self.settings_layout_v.addStretch()
         
        self.v_box_layout.addWidget(self.open_file_button)
        self.v_box_layout.addWidget(self.clear_button)
        self.v_box_layout.addWidget(self.Q_grafica.Qt_fig)
        

    # Button's functions

    def open_file_button_clicked(self):
        self.last_file_name, _ = QFileDialog.getOpenFileName()
        _ , extension = os.path.splitext(self.last_file_name)

        if self.last_file_name:
            with open(self.last_file_name, encoding='UTF-8', mode = 'r') as file:
                all_list = [line.strip() for line in file]

            format = identify_format(all_list)

            if format == 'text_file':
                self.show_new_window()  #New window for input user parameters.

            else:
                data = get_data(self.last_file_name)
                self.load_data(data)


    def clear_data_and_plots(self):
        self.Q_grafica.ax_perfil.clear()
        self.Q_grafica.ax_perfil_resta.clear()
        self.Q_grafica.ax_gamma.clear()
        self.Q_grafica.fig.canvas.draw()
        self.open_file_button.setEnabled(True)
        self.loaded_data = []

    def factor_button_clicked(self):
        scale_factor, ok = QInputDialog.getText(self, 'Scale factor', 'Scale factor:')
        try:
            scale_factor = float(scale_factor)
            if ok:
                self.loaded_data[-1][:,0] = self.loaded_data[-1][:,0] * scale_factor
                cache_data = self.loaded_data
                self.clear_data_and_plots()

                for data in cache_data:
                    self.load_data(data)

        except ValueError:
            QMessageBox().critical(self, "Error", "Enter a number.")
            print('Error, give a number.')

    def move_button_clicked(self):
        delta, ok = QInputDialog.getText(self, 'Scale factor', 'Origin displacement:')
        try:
            delta = float(delta)
            if ok:
                self.loaded_data[-1][:,0] = self.loaded_data[-1][:,0] + delta
                cache_data = self.loaded_data
                self.clear_data_and_plots()

                for data in cache_data:
                    self.load_data(data)

        except ValueError:
            QMessageBox().critical(self, "Error", "Enter a number.")
            print('Error, give a number.')        

    def show_new_window(self):
        start_word, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Start word:')
        if ok:
            data = get_data(self.last_file_name, start_word)
        else:
            data = get_data(self.last_file_name)
                
        self.load_data(data)
    
    #   Additional functions

    def load_data(self, data):
        
        self.loaded_data.append(data)       
        self.Q_grafica.plot_data(data)
        self.button_factor.setEnabled(True)
        self.button_origin.setEnabled(True)
        if len(self.loaded_data) == 2:
            self.calc_difference_and_gamma()

    def calc_difference_and_gamma(self):

        data_A = self.loaded_data[0]
        data_B = self.loaded_data[1]

        # Using interpolation, new values ​​of B are computed at positions given by A.
        data_B_from_A_positions = np.interp(data_A[:,0], data_B[:,0], data_B[:,1], left = np.nan)
    
        difference = data_A[:,1] - data_B_from_A_positions

        added_positions = np.array((data_A[:,0], difference))
        values = np.transpose(added_positions)
       
        g, g_percent = gamma_1D(
            data_A, 
            data_B,
            dose_t = float(self.dose_t_QLine.text()),
            dist_t = float(self.DTA_t_QLine.text()),
            dose_threshold = float(self.thres_QLine.text()),
            interpol = int(self.interp_QLine.text()),
            )

        self.Q_grafica.plot_resta(values)
        self.Q_grafica.plot_gamma(g)
        print(g_percent)

class Q_Base_Figure:
        
    def __init__(self):
        self.fig = Figure(figsize=(10,3), tight_layout = True, facecolor = 'whitesmoke')
        self.Qt_fig = FigureCanvas(self.fig)

        #   Axes para la imagen
        self.ax_perfil = self.fig.add_subplot(1, 2, 1)
        self.ax_perfil.set_ylabel('Percentage [%]')
        self.ax_perfil.set_xlabel('Distance [mm]')
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

def plot_profiles_and_comparison(
        P_ref, 
        P_eval,
        dose_t = 3, 
        dist_t = 2, 
        dose_tresh = 0, 
        interpol = 1
        ):
    """"
    A function to make a new window to show the given profiles, gamma and difference comparison.
    See relative_dose_1d.tools gamma_1d for gamma tolerance parameters.
    
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
            self.Q_grafica = Q_Base_Figure() 
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

    def plot_data(Profile):
        window.Q_grafica.plot_data(Profile)
    
    #def plot_gamma
    
    def show():
        sys.exit(app.exec())

    app = QApplication(sys.argv)
    window = Window()
    plot_data(P_ref)
    plot_data(P_eval)

if __name__ == '__main__':
    """
        from tools import build_from_array_and_step

        a = np.array([2,4,6,8,10])
        b = a + np.random.random_sample((5,))
        A = build_from_array_and_step(a, 0.5)
        B = build_from_array_and_step(b, 0.5)

        plot_profiles_and_comparison(A,B)
    """
    app = QApplication(sys.argv)
    window = Main_Window()
    sys.exit(app.exec())