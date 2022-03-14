import streamlit as st
import numpy as np
from Pages.page import Page
from config import Config
from scipy.optimize import linprog


def generate_linear_problem(dim, constraints_number):
    Config.objective = np.random.rand(dim)
    Config.constraints_A = np.random.randn(constraints_number, dim)
    bounds = np.zeros((dim, 2))
    bounds[:] = np.NAN
    Config.bounds = bounds
    Config.constraints_b = np.dot(Config.constraints_A, np.random.rand(dim))

    # Create bounds
    for i in range(dim):
        random_bounds = np.random.rand(2)
        rand = np.random.randint(4)
        # Rand=0: no bounds, rand=1: lower bound, rand=2: higher bound, rand=3: both bounds
        if rand == 1:
            Config.bounds[i][0] = random_bounds[0]
        if rand == 2:
            Config.bounds[i][1] = random_bounds[1]
        if rand == 3:
            if random_bounds[0] < random_bounds[1]:
                Config.bounds[i][0] = random_bounds[0]
                Config.bounds[i][1] = random_bounds[1]
            else:
                Config.bounds[i][1] = random_bounds[0]
                Config.bounds[i][0] = random_bounds[1]


class EllipsoidPage(Page):
    def show_page(self):
        st.write("""# Ellipsoid Method""")
        st.write("In this page you can choose the dimension of the objective of your linear problem and amount of "
                 "constraints (up to the dimension). After clicking the \"Generate Problem\" button, a linear problem "
                 "will be generated, the Ellipsoid method will run on the problem and the solution (named as 'x') will "
                 "be shown among some other important information about the solution such as the amount of iterations "
                 "needed (named as 'nit') and a message if the process finished succefully, if there is no answer, etc.")
        st.write("The problem that is generated contains an objective vector (in the wanted dimension), constraints "
                 "and bounds to each variable (the bounds can be limited or unlimited - nan value).")
        dim = st.number_input("Insert the maximum dimension: ", 1, 20, 3, 1)
        if dim > 20:
            st.error("Dimension is too high")
        if dim < 0:
            st.error("Dimension is less than 1")

        constraints_number = st.number_input("Insert the number of constraints: ", 1, dim, dim, 1)

        if st.button('Generate Problem'):
            generate_linear_problem(dim, constraints_number)

            st.write("##### The problem:")
            st.write(f'**Objective:** {Config.objective}')
            st.write(f'**Constraints - A (left side):** {Config.constraints_A}')
            st.write(f'**Constraints - b (right side):** {Config.constraints_b}')
            st.write(f'**Bounds:** {Config.bounds}')

            res = linprog(c=Config.objective, A_ub=Config.constraints_A, b_ub=Config.constraints_b,
                          bounds=Config.bounds, method='simplex')
            st.write(res)