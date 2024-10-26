from sys import path as syspath
from os import path as ospath
syspath.append(ospath.join(ospath.expanduser("~"),
                           '/home/ale/Desktop/py-matestlab/src'))

import numpy as np
import matplotlib.pyplot as plt

from pymatestlab.viewer import AbstractCurveViewer
from pymatestlab.util import load_dataset
from pymatestlab.discrete import DiscreteTestCurve


if __name__ == "__main__":

    x = np.linspace(1, 10, 20)
    x += np.random.random(size=x.shape)*5
    y = 5*x**2 + np.random.random(size=x.shape)*100

    d = DiscreteTestCurve(x=x, y=y)
    d.predict(np.linspace(1, 10, 20) )

    plt.plot(d.x,d.y, '-o')
    plt.plot(np.linspace(1, 20, 20), d.predict(np.linspace(1, 20, 20) ), '-o')
    plt.show()