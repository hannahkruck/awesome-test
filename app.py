"""Main module for the streamlit app"""
import streamlit as st

import awesome_streamlit as ast
import src.pages.about
import src.pages.gallery.index
import src.pages.home
import src.pages.resources
import src.pages.vision

ast.core.services.other.set_logging_format()

PAGES = {
    "welcome": src.pages.welcome,
    "home": src.pages.home,
    "detail": src.pages.gallery.detail,
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
