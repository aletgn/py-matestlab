import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
from pymatestlab.util import diff_mask, is_sorted, line, line_pars


class DiscreteTestCurve:
    """Piece-wise interpolation of curves."""

    def __init__(self, x, y, name="Untitled") -> None:
        self.x = x
        self.y = y
        self.name = name
        self.check_sorted()

    def check_sorted(self):
        if is_sorted(diff_mask(self.x)):
            print("x is sorted")
        else:
            print("x is unsorted")
            self.sort_data()
            print(f"Sorted: {is_sorted(diff_mask(self.x))}")

    def sort_data(self):

        x_sorted = self.x
        y_sorted = self.y

        while not is_sorted(diff_mask(x_sorted)):
            mask = diff_mask(x_sorted)
            # print(mask)
            x_sorted = x_sorted[mask]
            y_sorted = y_sorted[mask]
            # print(x_sorted)
            # print(np.diff(x_sorted, prepend=True) > 0)
            # print()

        self.x = x_sorted
        self.y = y_sorted

    def predict_point(self, x):
        mask = self.x < x
        print(mask)

        if x > self.x.max():
            print("Extrapolation beyond right edge")
            p1 = (self.x[-2], self.y[-2])
            p2 = (self.x[-1], self.y[-1])

        elif x < self.x.min():
            print("Extrapolation beyond left edge")
            p1 = (self.x[0], self.y[0])
            p2 = (self.x[1], self.y[1])

        else:
            print("Intepolation")
            x_break = self.x[mask]
            # len_x = len(x)
            p1 = (self.x[len(x_break)-1], self.y[len(x_break)-1])
            p2 = (self.x[len(x_break)], self.y[len(x_break)])

        print(p1, p2)
        return line(x, *line_pars(p1, p2))

    def predict(self, x_array):
        return [self.predict_point(x) for x in x_array]
