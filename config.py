import os
import pandas as pd

class Config:
    # Read the optimization method
    METHOD_1 = "Simplex"
    METHOD_2 = "Ellipsoid"
    methods_names = [METHOD_1, METHOD_2]

    method = "Method not found!"
    objective = "Objective not found!"
    constraints_A = "Constraints not found!"
    constraints_b = "Constraints not found!"
    bounds = "Bounds not found!"