import streamlit as st
from Pages.page import Page

class IntroductionPage(Page):
    def show_page(self):
        st.write("""# Optimization Final Project""")
        st.write("""## Simplex VS Ellipsoid Optimization Methods""")
        st.write("""### Introduction""")