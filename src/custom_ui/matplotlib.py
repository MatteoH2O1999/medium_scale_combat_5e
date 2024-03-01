import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PIL import Image


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.tight_layout(pad=0)
        super(MplCanvas, self).__init__(fig)

    def update_preview(self, fig: Figure):
        self.axes.clear()
        fig.tight_layout(pad=0)
        fig.canvas.draw()
        img = Image.frombytes(
            "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
        )
        plt.close(fig)
        self.axes.imshow(img)
        self.axes.set_axis_off()
        self.draw()
