import streamlit as st
from streamlit_extras.app_logo import add_logo

# Create a dictionary mapping page names to their corresponding functions

# Add a sidebar to select the page to display
# selected_page = st.sidebar.radio('Navigation', list(pages.keys()))
add_logo("./conagra.png", height=50)

# Run the selected page
# pages[selected_page]()