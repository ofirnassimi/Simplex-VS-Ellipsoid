import streamlit as st
import warnings
warnings.filterwarnings("ignore")
from Pages.introduction_page import IntroductionPage
from Pages.simplex_page import SimplexPage
from Pages.ellipsoid_page import EllipsoidPage
from Pages.tests_page import TestsPage

if __name__ == '__main__':
    st.sidebar.title("Simplex VS Ellipsoid Optimization Methods")
    menu = st.sidebar.radio('Navigation', ('Introduction', 'Simplex', 'Ellipsoid', 'Tests'))
    st.sidebar.title("Details")
    st.sidebar.info("Author: Ofir Nassimi")
    st.sidebar.info("This project compares between different optimization methods")
    st.sidebar.info("[Report](add url)")
    st.sidebar.info("[Github]()")

    introduction = IntroductionPage()
    simplex = SimplexPage()
    ellipsoid = EllipsoidPage()
    tests = TestsPage()

    if menu == 'Introduction':
        introduction.show_page()
    if menu == 'Simplex':
        simplex.show_page()
    if menu == 'Ellipsoid':
        ellipsoid.show_page()
    if menu == 'Tests':
        tests.show_page()