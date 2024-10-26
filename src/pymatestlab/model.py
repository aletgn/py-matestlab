from abc import ABC, abstractmethod
import numpy as np
from scipy.optimize import curve_fit

from pymatestlab.curve import TensileTestCurve
from pymatestlab.law import hooke, hollomon


class AbstractTensileModel(TensileTestCurve):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.par_keys = [] # sorted list of parameters -- nedeed for fit & pred
        self.par = None
        self.law = ...

    def fit(self, min_bound=None, max_bound=None):
        if min_bound is None:
            min_bound=[-np.inf]*len(self.par_keys)
        
        if max_bound is None:
            max_bound=tuple([np.inf]*len(self.par_keys))      
        
        self.par, _ = curve_fit(self.law, self.get_xy("x"), self.get_xy("y"),
                                bounds=(min_bound, max_bound))
        
        self.par_dict = dict(zip(self.par_keys, self.par))
        print(self.par_dict)

    def predict(self, x, in_place=True):
        pred_stress = self.law(x, *self.par)
        if in_place:
            self.stress = pred_stress
        else:
            data_dict = {"strain": x, "stress": pred_stress}
            label_dict = {**data_dict, **self.par_dict}
            return TensileTestCurve(**label_dict)


class HookeModel(AbstractTensileModel):

    def __init__(self, **kwargs) -> None:
        try:
            self.E = kwargs.pop("E")
        except KeyError:
            self.E = None
        super().__init__(**kwargs)
        self.par_keys = ["E"]
        self.law = hooke


class HollomonModel(AbstractTensileModel):

    def __init__(self, **kwargs) -> None:
        try:
            self.K = kwargs.pop("K")
            self.n = kwargs.pop("n")
        except KeyError:
            self.K = None
            self.n = None
        super().__init__(**kwargs)
        self.par_keys = ["K", "n"]
        self.law = hollomon