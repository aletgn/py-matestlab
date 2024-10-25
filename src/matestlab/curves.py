from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt


class AbstractTestCurve(ABC):

    def __init__(self, **kwargs) -> None:
        """Acts as a factory design pattern."""
        self.labels = []

        try:
            self.name = kwargs.pop("name")
        except KeyError:
            self.name = kwargs.pop("Untitled")

        for k, v in kwargs.items():
            setattr(self, k, v)
            self.labels.append(k)

        self.edges()
    
    def edges(self):
        for l in self.labels:
            setattr(self, l + "_min", getattr(self, l).min())
            setattr(self, l + "_max", getattr(self, l).max())

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

    def true_2_eng(self, in_place=True):
        eng_stress = self.stress / (1 + self.strain)
        eng_strain = np.exp(self.strain) 

        if in_place:
            self.strain = eng_strain
            self.stress = eng_stress
        else:
            label_dict = {"name": self.name + "_Eng",
                          "strain": eng_strain,
                          "stress": eng_stress}
            print(label_dict)
            return TensileTestCurve(**label_dict)

    def eng_2_true(self, in_place=True):
        true_stress = self.stress * (1 + self.strain)
        true_strain = np.log1p(self.strain)
                
        if in_place:
            self.strain = true_strain
            self.stress = true_stress
        else:
            label_dict = {"name": self.name + "_True",
                          "strain": true_strain,
                          "stress": true_stress}
            print(label_dict)
            return TensileTestCurve(**label_dict)



if __name__ == "__main__":
    # test = TensileTestCurve(name="tensile", strain=strain, stress=stress)
    # plt.figure()
    # plt.plot(test.strain, test.stress)

    # tt = test.eng_2_true(in_place=False)
    # plt.plot(tt.strain, tt.stress)
    # plt.show()
    ...

