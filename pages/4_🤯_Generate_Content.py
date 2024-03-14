import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.card import card
from streamlit_extras.grid import grid
import pandas as pd
from io import StringIO
import time

def fetch_data():
    # Sample data for demonstration
    return [
    {
        'title': 'Plant-Powered Protein Bowl',
        'description': 'A nutritious and satisfying bowl featuring a blend of quinoa, roasted vegetables, chickpeas, and a creamy tahini dressing.'
    },
    {
        'title': 'Fruit Infused Sparkling Water',
        'description': 'Refreshing sparkling water infused with natural fruit flavors such as watermelon, lime, and berries for a burst of hydration and taste.'
    },
    {
        'title': 'Gourmet Avocado Toast',
        'description': 'Artisanal sourdough bread topped with creamy avocado slices, heirloom tomatoes, microgreens, and a drizzle of balsamic glaze.'
    }
]



def app():
    st.header('CAG PIE Content Generation :pie:', divider='green')
    st.subheader("Welcome to the Emerging Food Items Generation section! In this section, we utilize the insights gleaned from our data analysis to generate new and emerging food items. By leveraging advanced algorithms and machine learning techniques, we uncover innovative combinations, flavors, and trends that are shaping the future of the food industry.")

    st.info('This is a purely informational message', icon="ℹ️")
    
    generated_products = fetch_data()

    with st.form("my_form"):

        st.write("Content Generation Part One")

        selected_data_sources = st.multiselect(
            'Select Data Source(s)',
            ['Frozen Breakfast', 'Frozen Handhelds', 'Frozen Dessert']
        )

        selected_categories = st.multiselect(
            'Select Target Attributes',
            ['Frozen', 'Handhelds', 'Healthy', 'Crunchy']
        )

        category = st.selectbox('Select Food Category', ['Breakfast', 'Lunch', 'Dinner', 'Dessert'])

        target_age_demographic = st.slider(
            'Target Age Demographic',
            min_value=10,
            max_value=75,
            value=(15, 35),
            step=1,
        )

        target_prep_time = st.slider(
            'Target Preperation Time (min)',
            min_value=0,
            max_value=10,
            value=(2, 5),
            step=1,
        )

        # Text input for name
        additional_info = st.text_area('Additional Information', '')
        submitted = st.button("Create my baller food", use_container_width=True)

    if submitted:
        with st.spinner('Generating your le erm EPIC food creationz! ~'):
            time.sleep(1)
        
        st.success('Ermmmm... your ideas are flippin HERE!')
        for i, item in enumerate(generated_products):
            container = st.container(border=True)
            container.write(f"### Product {i+1}\n{item['title']}\n\n**Description**\n{item['description']}")
        st.divider()
        
        

if __name__ == '__main__':
    app()