from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class AbstractCurveViewer():

    def __init__(self, **kwargs) -> None:
        try:
            self.name = kwargs.pop("name")
        except KeyError:
            self.name = kwargs.pop("Untitled")

    def inspect_curve(self, *curves):
        fig, ax = plt.subplots(dpi=300)
        for c in curves:
            ax.plot(c.get_xy("x"), c.get_xy("y"), color=c.color,
                    linestyle = c.linestyle, linewidth=c.linewidth,
                    marker=c.marker, markersize=c.markersize)
        plt.show()
