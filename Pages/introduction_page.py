import streamlit as st
from Pages.page import Page

class IntroductionPage(Page):
    def show_page(self):
        st.write("""# Optimization Final Project""")
        st.write("""## Simplex VS Ellipsoid Optimization Methods""")
        st.write("""### Introduction""")
        st.write("In this project we will see the differences between 2 major methods in the optimization world: "
                 "Simplex and Ellipsoid. Each method is well-known for it's ability to handle mainly LP problems but "
                 "each one of them has different advantages, as well as disadvantages.")
        st.write("So, in this website we can test the Simplex method which is, until these days, the best one in "
                 "optimizations of LP problems. One of the known down-sides of this method is it's ability to solve a "
                 "Klee-Minty cube. Finding the lengths of the cube is a pretty hard problem for Simplex, but the "
                 "Ellipsoid method is known for the ability of it to solve this problem much faster.")
        st.write("This website contains 4 pages. The first one is the Introduction page, which you are currently in, "
                 "another 2 pages, one for each method, named Simplex and Ellipsoid, where you can create your own "
                 "problem and see it's solution by solving it with the specific method. The 3rd page, the tests page, "
                 "is for creating many problems of both types mentioned above and analyzing their solutions.")