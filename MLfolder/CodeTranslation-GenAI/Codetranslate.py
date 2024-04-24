import streamlit as st
import requests
import json

# Replace with your actual API endpoint URL
API_ENDPOINT = ""

# Set page configuration with dark theme
st.set_page_config(
    page_title="Translation App",
    page_icon=":globe_with_meridians:",
    #theme="dark"
)

st.title("Language Translator :globe_with_meridians:")

# Language options
languages = ["C++", "Visual Basic", "Python", "C#", "Java"]

# Containers for Input and Output
input_container = st.container()
output_container = st.container()

with input_container:
    st.subheader("Code Input")
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        source_text = st.text_area("Base Code", placeholder="Enter code to translate...", height=200)
        base_language = st.selectbox("Base Language", languages)

    with col2:
        st.empty()
        translate_button = st.button("Translate :arrow_right:")

    with col3:
        translated_text = st.text_area("Converted Code", placeholder="Translation will appear here...", height=200)
        target_language = st.selectbox("Target Language", languages)

# Validation
if base_language == target_language:
    st.error("Base and target languages must be different.")
else:
    if translate_button:
        if source_text:
            # Prepare data in JSON format
            data = {
                "source_text": source_text,
                "base_language": base_language,
                "target_language": target_language
            }

            # Send POST request with JSON data
            headers = {"Content-Type": "application/json"}
            response = requests.post(API_ENDPOINT, json=data, headers=headers)
            print('data :', data)
            if response.status_code == 200:
                try:
                    # Parse response JSON and update translated_text
                    response_json = response.json()
                    translated_text.value = response_json["translated_text"]
                except json.JSONDecodeError:
                    st.error("Invalid JSON response from the server.")
                    print("Response content:", response.content)
            else:
                st.error("Translation failed. Please try again later.")
        else:
            st.warning("Please enter code to translate.")
