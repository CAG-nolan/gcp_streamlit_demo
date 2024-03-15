import streamlit as st
from streamlit_extras.app_logo import add_logo
from services.NPDWrapper import NPDWrapper
from services.ImageGeneration import ImageGeneration
import streamlit.components.v1 as components
from streamlit_extras.stateful_chat import chat

from pandas import DataFrame
import csv
import requests

st.set_page_config(layout="wide", page_icon="./conagra.png", initial_sidebar_state="collapsed")

def progress_form_one():
    st.session_state.form_one_done = True

def progress_form_two():
    st.session_state.form_two_done = True
    st.session_state.generate_button_disabled = True

def progress_form_three(title, description, reason):
    st.session_state.form_three_done = True
    if "concept_title" not in st.session_state:
        st.session_state.concept_title = title
    if "concept_description" not in st.session_state:
        st.session_state.concept_description = description
    if "concept_reason" not in st.session_state:
        st.session_state.concept_reason = reason
def image_card(base64_image):
    st.markdown(f'<div><img class="img-fluid" width="100%" height="280" alt="100%x280" src="data:image/jpeg;base64,{base64_image}"></div>')
def render_card(title, description, reason, btn_key):
    """
    Render a card with title, description, and image.
    """
    new = st.container(border=True)
    new.header(title, divider="gray")
    new.write(description)
    new.success(reason, icon="✅")
    new.button(label="Generate Content →", key=btn_key, use_container_width=True, on_click=progress_form_three, args=[title, description, reason])

def restart():
    st.session_state.form_one_done = False
    st.session_state.form_two_done = False
    st.session_state.form_three_done = False
    st.session_state.generate_button_disabled = False
    st.session_state.messages = []

def initialize_state():
    if "form_one_done" not in st.session_state:
        st.session_state.form_one_done = False
    if "form_two_done" not in st.session_state:
        st.session_state.form_two_done = False
    if "form_three_done" not in st.session_state:
        st.session_state.form_three_done = False
    if "generate_button_disabled" not in st.session_state:
        st.session_state.generate_button_disabled = False
    if "infer_data" not in st.session_state:
        st.session_state.infer_data = False
    if "messages" not in st.session_state:
        st.session_state.messages = []

add_logo("./conagra.png", height=50)

initialize_state()

labels = {
    "Prep1to5Min": "One to Five Minute Prep",
    "PrepNoneMin": "Zero Minute Prep",
    "Prep5to14Min": "Five to Fifteen Minute Prep",
    "Prep15PlusMin": "Prep Time Greater Than 15 Minutes"
}

def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return value
    
# Custom function to create a data metric with custom color
def custom_metric(value, label, color, tag, wrapper):
    wrapper.markdown(
        f'<div style="border-left: 5px solid {color}; padding-left: 1em; margin-top: 1em; margin-bottom: 1em;">'
        f'<div font-size: 28px;>{label}</div>'
        f'<div style="color: {color}; font-size: 36px;">{value}<span style="font-size: 16px;">% {tag}</span></div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.title("Conagra and Google Hackathon")

if not st.session_state.form_one_done:
    # Load the container about the IRI and NPD data
    form_part_one = st.container(border=True)
    with form_part_one:
        npd_wrapper = NPDWrapper()
        
        df:DataFrame = npd_wrapper.return_dataframe()
        # Find the column with the maximum value in each row
        max_columns = df.iloc[:, 1:].idxmax(axis=1)

        # Find the maximum value in each row
        max_values = df.iloc[:, 1:].max(axis=1)

        min_columns = df.iloc[:, 1:].idxmin(axis=1)
        # Find the minimum value in each row
        min_values = df.iloc[:, 1:].min(axis=1)

        st.header('NPD Data Summarization', divider='gray')

        # Combine results into a DataFrame
        result_df = DataFrame({'Min_Column': min_columns, 'Min_Value': min_values, 'Max_Column': max_columns, 'Max_Value': max_values})
        
        col1, col2, col3= st.columns(3)

        successful_attributes = {
                "prompt": f"Based on this dataframe, what is the highest category and cooktime for consumers. The values represent the percentage of responders who answered in that category. Briefly explain why: {df}",
            }
        successful_attributes = requests.post(url="http://127.0.0.1:6969/api/prompt/chat", json=successful_attributes)

        negative_attributes = {
                "prompt": f"Based on this dataframe, what is the lowest category and cooktime for consumers. The values represent the percentage of responders who answered in that category. Briefly explain why: {df}",
            }
        negative_attributes = requests.post(url="http://127.0.0.1:6969/api/prompt/chat", json=negative_attributes)


        for index, row in result_df.iterrows():
            if index == 0:
                with col1:
                    tag = "Over 18 Years Old"
                    custom_metric(f"{row[3]}", labels.get(row[2]), "green", tag, st)
                    custom_metric(f"{row[1]}", labels.get(row[0]), "red", tag, st)
            else:
                with col2:
                    tag = "Under 18 Years Old"
                    custom_metric(f"{row[3]}", labels.get(row[2]), "green", tag, st)
                    custom_metric(f"{row[1]}", labels.get(row[0]), "red", tag, st)
        with col3:
            st.success(successful_attributes.text)
            st.error(negative_attributes.text)
        
        st.header('IRI Data Communication', divider='gray')
        
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

      
        # React to user input
        if prompt := st.chat_input("Ask questions related to data..."):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = f"Echo: {prompt}"
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.button("Next Section", on_click=progress_form_one)
            
# st.write(npd_wrapper.return_dataframe())
if st.session_state.form_one_done and not st.session_state.form_three_done:   
    form_part_two = st.container(border=True)
    with form_part_two:      
        st.header('Generate New Products', divider='gray')
            
        selected_categories = st.multiselect(
            'Select Target Categories',
            ['Frozen', 'Handhelds', 'Healthy', 'Crunchy']
        )

        selected_age = st.selectbox(
            'Select Target Age Group',
            ['Young Adults (<= 18)', 'Adults (> 18)']
        )

        target_prep_time = st.slider(
            'Target Preparation Time (min)',
            min_value=0,
            max_value=10,
            value=(2, 5),
            step=1,
        )

        additional = st.text_area(label="Any Additional Information")

        # Get the descriptors
        with open('data/ThemeData.csv', newline='') as csvfile:
            csv_data = csv.reader(csvfile, delimiter=',')
            csv_str = ""
            for row in csv_data:
                csv_str += str(row)

        positives = {
            "prompt": f"Find all the positive attributes of this csv file and return the result as a string paragraph. The data is here: {csv_str}",
        }
        positives = requests.post(url="http://127.0.0.1:6969/api/prompt/chat", json=positives)

        st.success(positives.text)

        negatives = {
            "prompt": f"Find all the negative attributes of this csv file and return the result as a string paragraph. The data is here: {csv_str}",
        }
        negatives = requests.post(url="http://127.0.0.1:6969/api/prompt/chat", json=negatives)

        st.error(negatives.text)

        trends = {
            "prompt": f"Based on the given csv file, infer if there are any trends in the data. The data is here: {csv_str}",
        }
        trends = requests.post(url="http://127.0.0.1:6969/api/prompt/chat", json=trends)

        st.info(trends.text)

        st.button("Generate Items", on_click=progress_form_two, disabled=st.session_state.generate_button_disabled)

    # Load the image content generation tooling
    if st.session_state.form_two_done and not st.session_state.form_three_done:
        form_image_viewer = st.container(border=True)
        with form_image_viewer:      
            st.header('Generate New Products', divider='gray')

            data = {
                "form": selected_categories,
                "age": selected_age,
                "likes": positives.text,
                "dislikes": negatives.text,
                "additional": additional,
                "trends": csv_str
            }

            col1, col2, col3= st.columns(3)

            with col1:
                concept = requests.post(url="http://127.0.0.1:6969/api/prompt/generate", json=data)
                concept = concept.json()
                render_card(concept.get("title"), concept.get("description"), concept.get("reasoning"), btn_key="next_one")

            with col2:
                concept = requests.post(url="http://127.0.0.1:6969/api/prompt/generate", json=data)
                concept = concept.json()
                render_card(concept.get("title"), concept.get("description"), concept.get("reasoning"), btn_key="next_two")

            with col3:
                concept = requests.post(url="http://127.0.0.1:6969/api/prompt/generate", json=data)
                concept = concept.json()
                render_card(concept.get("title"), concept.get("description"), concept.get("reasoning"), btn_key="next_three")


if st.session_state.form_three_done:
    form_part_three = st.container(border=True)
    with form_part_three:  
        col1, col2, col3= st.columns(3)
        with col1:
            data = {
                    "title": st.session_state.concept_title,
                    "description": st.session_state.concept_description,
                    "additional": "",
                }
            concept = requests.post(url="http://127.0.0.1:6969/api/image/generate", json=data)
            concept = concept.json()
            st.image(concept['image'], caption=st.session_state.concept_title, use_column_width=True)
        with col2:
            data = {
                    "title": st.session_state.concept_title,
                    "description": st.session_state.concept_description,
                    "additional": "MAKE THE CONTENT APPEAR LIKE IT WOULD IN CONSUMER READY PACKING. THIS PACKAGING CAN BE EITHER PLASTIC CUPS, PLASTIC SLEEVES, etc. IT IS IMPORTANT THAT THE PRODUCT IS SHOWN IN A CONSUMER-READY PACKAGE SIMILAR TO WHAT WOULD BE FOUND ON THE SHELF AT A GROCERY STORE!",
                }
            concept = requests.post(url="http://127.0.0.1:6969/api/image/generate", json=data)
            concept = concept.json()
            st.image(concept['image'], caption=st.session_state.concept_title, use_column_width=True)
        with col3:
            data = {
                    "title": st.session_state.concept_title,
                    "description": st.session_state.concept_description,
                    "additional": "Make it look like it is from a commercial for food.",
                }
            concept = requests.post(url="http://127.0.0.1:6969/api/image/generate", json=data)
            concept = concept.json()
            st.image(concept['image'], caption=st.session_state.concept_title, use_column_width=True)
        st.button("Start Over", on_click=restart)