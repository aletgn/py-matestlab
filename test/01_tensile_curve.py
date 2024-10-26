from sys import path as syspath
from os import path as ospath
syspath.append(ospath.join(ospath.expanduser("~"),
                           '/home/ale/Desktop/py-matestlab/src'))

import numpy as np
import matplotlib.pyplot as plt

from pymatestlab.curve import TensileTestCurve
from pymatestlab.viewer import AbstractCurveViewer
from pymatestlab.util import load_dataset

if __name__ == "__main__":
    
    df = load_dataset("./00_synthetic_data.csv")
    tens_test = TensileTestCurve(name="01_Tensile_Curve",
                                 strain=df["strain"].to_numpy(),
                                 stress=df["stress"].to_numpy())
    
    v = AbstractCurveViewer(name="01_Tensile_Curve")
    v.inspect_curve(tens_test)


