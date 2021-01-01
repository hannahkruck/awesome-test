"""Main module for the streamlit app"""
import streamlit as st

import awesome_streamlit as ast
import src.pages.welcome
import src.pages.detail
import src.pages.home
import plotly.graph_objects as go
import pandas as pd
import altair as alt
from altair import Chart, X, Y, Axis, SortField, OpacityValue
import numpy as np

st.set_page_config(layout="wide")
ast.core.services.other.set_logging_format()

# Markdown to hide MainMenu (which contains things like rerun or links to github)
st.markdown('''
        <style>
            #MainMenu{
            display:none;
            }
        </style>
        ''', unsafe_allow_html=True)

ast.core.services.other.set_logging_format()

PAGES = {
    "Welcome": src.pages.welcome,
    "Map": src.pages.home,
    "Detail": src.pages.detail,
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)

if __name__ == "__main__":
    main()
