from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas

class Q_Graphic_Block:
        
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