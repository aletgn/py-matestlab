from abc import ABC, abstractmethod
import numpy as np
from pymatestlab.util import true_2_eng, eng_2_true

class AbstractTestCurve(ABC):

    def __init__(self, **kwargs) -> None:
        """Acts as a factory design pattern."""
        self.labels = []

        try:
            self.name = kwargs.pop("name")
        except KeyError:
            self.name = "Untitled"

        for k, v in kwargs.items():
            setattr(self, k, v)
            self.labels.append(k)

        self.edges()
        self.aspect()
    
    def edges(self):
        for l in self.labels:
            setattr(self, l + "_min", getattr(self, l).min())
            setattr(self, l + "_max", getattr(self, l).max())

    def aspect(self):
        self.color = 'k'
        self.linestyle = "-"
        self.linewidth =  1
        self.marker = 'o'
        self.markersize = 1.5

    @abstractmethod
    def get_xy(self, label):
        ...

    def translate(self, label, value, in_place=True):
        updated_value = getattr(self, label) + value
        
        if in_place:
            setattr(self, label, updated_value)
            self.edges()
        else:
            label_dict = {l: getattr(self, l) for l in self.labels}
            label_dict["name"] = self.name
            label_dict[label] = updated_value
            return AbstractTestCurve(**label_dict)
        
    def crop(self, label, min_value, max_value, in_place=True):
        data = getattr(self, label)
        mask = (data >= min_value) & (data <= max_value)
        
        if in_place:
            for l in self.labels:
                setattr(self, l, getattr(self, l)[mask])
        else:
            label_dict = {l: getattr(self, l)[mask] for l in self.labels}
            label_dict["name"] = self.name
            return AbstractTestCurve(**label_dict)
        

class TensileTestCurve(AbstractTestCurve):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        req_labels = {"stress", "strain"}
        if req_labels - set(self.labels):
            raise ValueError("Missing required parameters: strain, stress.")
        
    def get_xy(self, label):
        if label == "x":
            return self.strain
        elif label == "y":
            return self.stress
        else:
            raise KeyError("Must provide: x or y")

    def eng_curve(self, in_place=True):
        eng_strain, eng_stress = true_2_eng(self.strain, self.stress)

        if in_place:
            self.strain = eng_strain
            self.stress = eng_stress
            self.edges()
        else:
            label_dict = {"name": self.name + "_Eng",
                          "strain": eng_strain,
                          "stress": eng_stress}
            print(label_dict)
            return TensileTestCurve(**label_dict)

    def true_curve(self, in_place=True):
        true_strain, true_stress = eng_2_true(self.strain, self. stress)
                
        if in_place:
            self.strain = true_strain
            self.stress = true_stress
            self.edges()
        else:
            label_dict = {"name": self.name + "_True",
                          "strain": true_strain,
                          "stress": true_stress}
            print(label_dict)
            return TensileTestCurve(**label_dict)
