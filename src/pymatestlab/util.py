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