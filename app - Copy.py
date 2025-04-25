#health Management App
from dotenv import load_dotenv

load_dotenv() #load all local environment variables
import streamlit as st
import os
import google.generativeai as genai 
from PIL import Image

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

#funtion to load google gemini pro vision API and get response

def get_gemini_response(input, image,prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    # Call the Google Gemini API
    response =model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data= uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

input_prompt=""

st.set_page_config(page_title="AI Nutritionist App")
st.header("AI Nutritionist App")
input=st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.",  use_container_width=True)
submit=st.button("Tell me the total calories")

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response (input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)