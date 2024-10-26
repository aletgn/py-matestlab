from sys import path as syspath
from os import path as ospath
syspath.append(ospath.join(ospath.expanduser("~"),
                           '/home/ale/Desktop/py-matestlab/src'))

import numpy as np
import matplotlib.pyplot as plt

from pymatestlab.viewer import AbstractCurveViewer
from pymatestlab.util import load_dataset

from pymatestlab.model import HookeModel

if __name__ == "__main__":
    
    df = load_dataset("./00_synthetic_data.csv")

    h = HookeModel(name="02_HookeModel",
                   strain=df["strain"].to_numpy(), stress=df["stress"].to_numpy())
    
    # Extract linear regime data (see example 00_synthetic_data.py)
    h.crop("strain", -np.inf, 200/70000)
    h.fit()

    # Predict on different range and instantiate another model
    strain = np.linspace(h.strain.min(), h.strain.max(), 15)
    pred = h.predict(strain, in_place=False)
    pred.color="r"

    # display
    v = AbstractCurveViewer(name="02_Tensile_Curve")
    v.inspect_curve(h, pred)
