import numpy as np
import pandas as pd

def make_dataset(path, **kwargs):
    df = pd.DataFrame(kwargs)
    df.to_csv(path)

def load_dataset(path):
    return pd.read_csv(path)

def true_2_eng(true_strain, true_stress):
    return np.exp(true_strain), true_stress / (1 + true_strain)

def eng_2_true(eng_strain, eng_stress):
    return np.log1p(eng_strain), eng_stress * (1 + eng_strain)

def diff_mask(x):
    return np.diff(x, prepend=True) > 0

def is_sorted(diff):
    return np.all(diff)

def line(x, m, q):
    return m * x + q

def line_pars(p1, p2):
    slope = (p2[1] - p1[1])/(p2[0] - p1[0])
    intercept = p1[1] - slope * p1[0]
    assert intercept - (p2[1] - slope * p2[0]) < 0.001
    return slope, intercept