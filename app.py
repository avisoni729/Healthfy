import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd


# lets get thte api key from the environeent

gemini_api_key = 'Gemini_Api_key'

# Lets configure the model

model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key
)

st.title(":orange[Healthfyme:] :blue[ Your Personal Health assistant]")

st.markdown('''
            This app will give health advise, tailerd and customized to you only''')
tips= '''Follow the steps:
* Enter your details in sidebar
* Rate your activty and fitneess on the scale
* submit your details
* Lay back and see the magic happen
'''

# Design the sidebar for all the user parameters
st.sidebar.header(':red[ENTER YOUR DETAILS]')


name = st.sidebar.text_input('Enter your Name here')
gender = st.sidebar.selectbox('Eslect your gender',['Male','Female'])
age = st.sidebar.text_input('Enter your age')
weight = st.sidebar.text_input('Enter your weight in Kgs')
height = st.sidebar.text_input('Enter your height in cms')

bmi = pd.to_numeric(weight)/((pd.to_numeric(height)/100)**2)
active = st.sidebar.slider('Rate your activity level through out the week (0-5)',0,5,step=1)

fitness = st.sidebar.slider('Rate your fitness level (0-5)',0,5,step=1)

if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name}, your BMI is : {bmi} kg/m^2")
    
    
# Lets use the gemini model to generate the report

user_input = st.text_input('Ask your questions')

prompt = '''
<Role> You are an expert in health and wellness and has 10+ years experiance in guiding people 
<Goal> Generate the customized report addressing the problem the user has
<Context> Here are the details that the user has provided. Here is the question that user has asked : {user_input}.
name= {name}
age={age}
gender = {gender}
height = {height}
weight = {weight}
bmi= {bmi}
activity rating= {active}
fitnees rating = {ftness}

<Format> Following should be the format
* Start with the 2-3 line of comment on the details that user has provided
* Explain whaat the real problem could be in the bases of input the user provided.
* Suggesst the possible reasons for the problem.
* What are the possible solutions
* Mention the doctor from which specialization can be visited if required.
* Mention any changes in the diet which is required.
* In last create a final summary of all the things that has been discussed in the report
<Instructions> * Use bullet points wherever possible
* Create tables to present data where ever possible.
* Strictly do  not advise any medicine .
* You can provide some home remedies with caution.
'''

if st.button('Generate'):
    response = model.invoke(prompt)
    st.write(response.content)