import streamlit as st
from streamlit_extras.app_logo import add_logo

def app():
    st.title('Upload Content to GCP')
    st.subheader('Uploading Data to Google Cloud Platform for Content Generation with a Large Language Model')
    st.write('Google Cloud Platform provides a robust set of tools and services for storing and managing data in the cloud. By leveraging GCP\'s storage solutions, you can securely store your datasets and easily access them from anywhere in the world. This is particularly useful when working with Large Language Models, which often require large amounts of training data.')
    
    st.divider()
    st.write("### Data to Upload")
    st.write("Provide below the data which you would like to be included in the dataset. This can be HTML, PDF, XSLX, CSV, or Plain Text.")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
    st.divider()
    st.write("### Previously Uploaded Data")
    

if __name__ == '__main__':
    app()