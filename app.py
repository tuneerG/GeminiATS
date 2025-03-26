from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GENAI_API_KEY")
)

def get_gemini_response(input,pdf_content,prompt):
        model=genai.GenerativeModel("gemini-pro-vision"),
        response=model.generate_content(input,pdf_content[0],prompt)
        return response.text

def pdf_input_setup(uploaded_file):
    pdf_content = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = pdf_content[0]
    
    