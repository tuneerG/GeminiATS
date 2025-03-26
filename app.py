from dotenv import load_dotenv
load_dotenv()

import base64
import io

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

poppler_path = os.getenv("poppler_path")

genai.configure(
     api_key=os.getenv("GENAI_API_KEY")
)

# client=genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
        model=genai.GenerativeModel("gemini-2.0-flash")
        response=model.generate_content(f"{input},{pdf_content[0]},{prompt}")
        return response.text

def pdf_input_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_content = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = pdf_content[0]
        
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [{
            "mime_type" : "image/png",
            "data" :base64.b64encode(img_byte_arr).decode()
        }]
        
        return pdf_parts
    else:
        raise FileNotFoundError("File not found")
##Streamlit UI
st.set_page_config(page_title="AI Application Tracking System", page_icon="🔮", layout="wide")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("Resume uploaded successfully")

submit1 = st.button("Tell me about the resume")

# submit2 = st.button("How can I Improvise my skills")

# submit3 = st.button("What are the keywords missing from my resume")

submit4 = st.button("ATS Score")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=pdf_input_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit4:
    if uploaded_file is not None:
        pdf_content=pdf_input_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")