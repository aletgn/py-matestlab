# DISCLAIMER: THIS DATA IS SYNTHETIC AND USED FOR TESTING PURPOSES ONLY
from sys import path as syspath
from os import path as ospath
syspath.append(ospath.join(ospath.expanduser("~"),
                           '/home/ale/Desktop/py-matestlab/src'))

import numpy as np
import pandas as pd
from pymatestlab.util import make_dataset

youngs_modulus = 70e3  # Young's Modulus in MPa
yield_strength = 200   # Yield strength in MPa
uts = 350              # Ultimate tensile strength in MPa
strain_at_uts = 0.15   # Strain at UTS (15%)

# hardening -- Hollomon
K = 200
n = 0.7

# Elastic region
strain_elastic = np.linspace(0, yield_strength/youngs_modulus, 20)
stress_elastic = youngs_modulus * strain_elastic
# Plastic region to UTS
strain_plastic = np.linspace(yield_strength/youngs_modulus, strain_at_uts, 1000)
stress_plastic = yield_strength + K*((strain_plastic - strain_plastic[0])**n)

from pymatestlab.util import load_dataset
from pymatestlab.curve import TensileTestCurve
from pymatestlab.viewer import AbstractCurveViewer


if __name__ == "__main__":

    strain = np.concatenate([strain_elastic, strain_plastic])
    stress = np.concatenate([stress_elastic, stress_plastic])
    make_dataset("./00_synthetic_data.csv", strain=strain, stress=stress)

    df = load_dataset("./00_synthetic_data.csv")
    tens_test = TensileTestCurve(name="01_Tensile_Curve",
                                 strain=df["strain"].to_numpy(),
                                 stress=df["stress"].to_numpy())
    
    v = AbstractCurveViewer(name="01_Tensile_Curve")
    v.inspect_curve(tens_test)