import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Pages.page import Page
from config import Config
from scipy.optimize import linprog

def generate_linear_problem(dim, constraints_number):
    Config.objective = np.random.rand(dim)
    Config.constraints_A = np.random.randn(constraints_number, dim)
    Config.constraints_b = np.dot(Config.constraints_A, np.random.rand(dim))
    bounds = np.zeros((dim, 2))
    bounds[:] = np.NAN
    Config.bounds = bounds

def generate_klee_minty_cube(dim):
    # Create objective of the cube
    obj = np.full((dim), 2)
    j = dim - 1
    for i in range(dim):
        obj[i] = obj[i] ** i
        j -= 1
    Config.objective = obj

    # Create matrix constraints (left-hand side of the constraints)
    A = np.zeros((dim, dim))
    for i in range(dim):
        k = 0
        for j in range(i, -1, -1):
            A[i][j] = 2 ** k
            if (k == 0):
                k += 2
            else:
                k += 1
    Config.constraints_A = A

    # Create right side of the constraints
    b = 5 * np.ones((dim))
    for i in range(dim):
        b[i] = b[i] ** (i + 1)
    Config.constraints_b = b

    # Create bounds
    bounds = np.zeros((dim, 2))
    bounds[:, 1] = np.NaN
    Config.bounds = bounds


class TestsPage(Page):
    def show_page(self):
        st.write("""# Simplex VS Ellipsoid""")
        st.write("""#### Tests Page""")
        st.write("In order to check the abilities of each method, we will run in this page 2 types of problems on each "
                 "algorithm. The first one is the linear problem and the second one is the Klee-Minty Cube.")
        st.write("The program generates 500 different linear problem and runs them both on the Simplex algorithm and "
                 "the Ellipsoid algorithm. After running all of the 500 problems on one algorithm, the average number "
                 "of iterations will be calculated, as well as the total number of the 500 problems. Watching the "
                 "number of iterations of each algorithm can help us understand better the efficiency of each one of "
                 "them and compare them. In the second part, the same Klee-Minty cube runs on both algorithms as well "
                 "but in 15 dimensions, from 1 dimension to 15. In this part the average and total iterations of each "
                 "method are being calculated and shown as well. At the end, graphs that summarize all of the tests are "
                 "shown.")

        #NUM_PROBLEMS = 100
        NUM_PROBLEMS = 500

        total_iterations_simplex = 0
        total_iterations_ellipsoid = 0
        total_iterations_cube_simplex = 0
        total_iterations_cube_ellipsoid = 0
        all_linear_problems = []

        linear_simplex_iters = []
        linear_ellipsoid_iters = []
        km_simplex_iters = []
        km_ellipsoid_iters = []

        # First, generate linear problems
        for i in range(NUM_PROBLEMS):
            dim = np.random.randint(1, 21)
            constraints_number = np.random.randint(1, dim + 1)
            generate_linear_problem(dim, constraints_number)
            all_linear_problems.append([Config.objective, Config.constraints_A, Config.constraints_b, Config.bounds])

        if st.button('Start test'):
            st.write("Testing linear problems with Simplex algorithm...")
            i = 0
            for problem in all_linear_problems:
                i += 1
                res = linprog(c=problem[0], A_ub=problem[1], b_ub=problem[2], method='simplex')
                """if (i % 100 == 0):
                    st.write(problem)
                    st.write(res)"""
                iterations = res['nit']
                total_iterations_simplex += iterations
                #linear_simplex_iters.append(iterations)
                linear_simplex_iters.append(total_iterations_simplex)
                message = res['message']
            average_iterations = total_iterations_simplex / NUM_PROBLEMS
            st.write(f'Average number of iterations: {average_iterations}')
            st.write(f'Total number of iterations: {total_iterations_simplex}')

            st.write("Testing linear problems with Ellipsoid algorithm...")
            i = 0
            print()
            for problem in all_linear_problems:
                i += 1
                res = linprog(c=problem[0], A_ub=problem[1], b_ub=problem[2], method='interior-point')
                """if (i % 100 == 0):
                    st.write(problem)
                    st.write(res)"""
                iterations = res['nit']
                total_iterations_ellipsoid += iterations
                #linear_ellipsoid_iters.append(iterations)
                linear_ellipsoid_iters.append(total_iterations_ellipsoid)
            average_iterations = total_iterations_ellipsoid / NUM_PROBLEMS
            st.write(f'Average number of iterations: {average_iterations}')
            st.write(f'Total number of iterations: {total_iterations_ellipsoid}')

            st.write("Testing Klee-Minty Cube with Simplex algorithm...")
            for i in range(15):
                generate_klee_minty_cube(i + 1)
                res = linprog(c=Config.objective, A_ub=Config.constraints_A, b_ub=Config.constraints_b,
                              bounds=Config.bounds, method='simplex')
                iterations = res['nit']
                total_iterations_cube_simplex += iterations
                km_simplex_iters.append(total_iterations_cube_simplex)
            average_iterations = total_iterations_cube_simplex / 15
            st.write(f'Average number of iterations: {average_iterations}')
            st.write(f'Total number of iterations: {total_iterations_cube_simplex}')

            st.write("Testing Klee-Minty Cube with Ellipsoid algorithm...")
            for i in range(15):
                generate_klee_minty_cube(i + 1)
                res = linprog(c=Config.objective, A_ub=Config.constraints_A, b_ub=Config.constraints_b,
                              bounds=Config.bounds, method='interior-point')
                iterations = res['nit']
                total_iterations_cube_ellipsoid += iterations
                km_ellipsoid_iters.append(total_iterations_cube_ellipsoid)
            average_iterations = total_iterations_cube_ellipsoid / 15
            st.write(f'Average number of iterations: {average_iterations}')
            st.write(f'Total number of iterations: {total_iterations_cube_ellipsoid}')

            # Show graphs
            nums = []
            for i in range(NUM_PROBLEMS):
                nums.append(i + 1)

            nums2 =[]
            for i in range(15):
                nums2.append(i + 1)

            st.write("#### Graphs")
            st.write("This graph shows the total iterations of each algorithm in relation to the number of tests on "
                     "the linear problems that were created above.")
            fig, ax = plt.subplots()
            plt.plot(nums, linear_simplex_iters, marker=".")
            plt.plot(nums, linear_ellipsoid_iters, marker=".")
            plt.legend(['Simplex Method', 'Ellipsoid Method'])
            plt.xlabel("Test")
            plt.ylabel("Total Iterations")
            plt.title("Total Iterations of Linear Problems in Both Methods")
            st.pyplot(fig)
            st.markdown("""""")

            st.write("This graph shows the total iterations of each algorithm in relation to the number of tests on "
                     "the Klee-Minty Cube problems that were created above.")
            fig, ax = plt.subplots()
            plt.plot(nums2, km_simplex_iters, '.-')
            plt.plot(nums2, km_ellipsoid_iters, '.-')
            plt.legend(['Simplex Method', 'Ellipsoid Method'])
            plt.xlabel("Test")
            plt.ylabel("Total Iterations")
            plt.title("Total iterations of Klee-Minty Cubes in Both Methods")
            st.pyplot(fig)
            st.markdown("""""")