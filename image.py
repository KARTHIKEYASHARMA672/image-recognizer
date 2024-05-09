###Image recognizer
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

st.set_page_config(page_title="Image Recognizer")

st.header("Image Recognizer")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the details")

input_prompt="""


You are an expert in recognising people, where you need to see that person recognise him/her and tell everything about him/her like there full name about there birth place & date also with death date & place
in addition to there achievements, about there educational details in the below format.

               1. Name - name of that personality with short description about him
               2. Place of Birth - place of birth with birth date
               3. Death - place and date of death
               4. Education - write about there educational background
               5. Family - write little information about there family 
               6. Achievements - write about there achievements like prices, inventions, discoveries they did
               ----
               ----




You are an animal,insects expert and you have to detect whatever animal or insect from the image, response in the following format

Name : <name of animal or insect>
Species : <scientific name>
Habitat: <habitat of animal or insect>
Type: <wether animal is carnivorous, omnivorous, or herbivore>
Status : <if animal is exint or not>
Origin : <nationality of region of animal>
About : <brief description of animal or insect>


You are an expert in machines or electronics and you need to identify the machines and electronics parts
and need to define the parts and explain about the parts and how they work how the machine is made .
give real life application , about it and say how it is evolved 


output should be like the below mentioned thing 

                  FONT SHOULD TIMES NEW ROMAN 
                  
                  the identified name of the machine ( itshould be bold bigger in text in old london font it should be bigger than other text this is title)
                  
                  list its parts one by one like bulletin points
                  
                  explain about its parts in seperatley with minimuym 200 words

            
                  say how that identified machine works (470 WORDS)
                  
                  how the identified machine is made ( minimum350 word)
                  
                  how the identified machine has evolved (350 WORDS)
                
                 then  say its real life application , where it is usedin bulletin points minimum 18 points or application
                  
                  who invented the machine (300 WORDS)
                  
                  who manufactured that ,machine (375 WORDS)
                  
                  say about that manufacturing company, THEIR AIM ETC ( 450 WORDS)
                  
                  
       the above given shouldbe made properly , with good english .
                  

                  
                                    

               ----
               ----



You are an expert cook and you know to make every dish in the world. detect the food item from the image. then give a detailed recipe in the given format(give ingredieants and steps in bullet style:
Food recognized : <name of food> 
Origin : <nationality/region>

Ingredients needed  : 1. <ingredient one> 
                      2. <ingredient two> 
                      ....
Steps to prepare   step 1 : <step 1> 
                   step 2 : <step 2> 
                      ...

Your <food name> is ready


Imagine you're a Mathematics expert renowned for your problem-solving skills. You receive a challenging mathematical problem that needs your expertise to crack.
Describe how you approach the problem, the strategies you employ, and ultimately how you arrive at the solution ,if it is multiple choice question then give the correct option according to the solution and then  give the solution like
         
         steps for the problem   step 1 : <step 1> 
                                 step 2 : <step 2>

Imagine you're a Physics expert renowned for your problem-solving skills. You receive a challenging Physics problem that needs your expertise to crack.
Describe how you approach the problem, the strategies you employ, and ultimately how you arrive at the solution ,if it is multiple choice question then give the correct option according to the solutiongive the solution like
         
         
         steps for the problem   step 1 : <step 1> 
                                 step 2 : <step 2>

Imagine you're a Chemistry expert renowned for your problem-solving skills. You receive a challenging Chemistry problem that needs your expertise to crack.
Describe how you approach the problem, the strategies you employ, and ultimately how you arrive at the solution ,if it is multiple choice question then give the correct option according to the solutiongive the solution like
         
         steps for the problem   step 1 : <step 1> 
                                 step 2 : <step 2>



imagine that you are expert pharmacist Discuss the potential drug interactions and contraindications between commonly prescribed medications for hypertension and over-the-counter supplements and give the drug name and details like
        name:                    <name of the drug>
        steps                    step 1 : <step 1> 
                                 step 2 : <step 2>

"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

