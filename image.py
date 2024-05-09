### Image recognition
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("AIzaSyDt9PK2goi-jk9hZW9SOF6JoNnAMg_SmeY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Image recognition")

st.header("Image recognition")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the Details")

input_prompt="""
You are an expert in mobiles and electronics and you need to identify the mobile and its parts
and need to define the parts and explain about the parts like battery,camera ,sound system, display,
ram , processor, 4g or 5g .
out put should br like the below moentioned format 
                  FONT SHOULD TIMES NEW ROMAN
                   list its parts one by one like bulletin points
                   explain about its parts in seperatley with minimum 100 words
                   who manufactured that ,machine (200 WORDS)
                   say about that manufacturing company, THEIR AIM ETC ( 150 WORDS)
    the above given should be made properly , with good english
    

    ----
    ----
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
 You are an expert cook and you know to make every dish in the world. detect the food item from the image. then give a detailed recipie in the given format(give ingredieants and steps in bullet style:
Food recognized : <name of food> 
Origin : <nationality/region>

Ingredients needed  : 1. <ingredient one> 
                      2. <ingredient two> 
                      ....
Steps to prepare   step 1 : <step 1> 
                   step 2 : <step 2> 
                      ...

Your <food name> is ready

You are an expert  identifing  the companies and need to define the details of the company
like Founder,Business Diversification,Key Companies, Global Presence,Social Responsibility,
Leadership and Governance,Innovation and sutainability,acquisitions. provided
out put should br like the below mentioned format.
                  FONT SHOULD TIMES NEW ROMAN
                   list its parts one by one like bullet in points
                   explain about  each seperatley with minimum 100 words
    the above given should be made properly , with good english

    ----
    ----

you are expert in human gender identification you need to identify the gender of the person from the image and give the details according to this requirements
                 name:
                 adhaar no:
                 phone number:


    ----
    ----

    


"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

