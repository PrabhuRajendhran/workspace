import streamlit as st
import anthropic
import io
import os
import re
import json
import time
import boto3
import base64
import PyPDF2
import string
import random
import mammoth
import pdfplumber
import pandas as pd
import streamlit as st
from docx import Document
from requests import request

def show_csv(uploaded_file):
    # Display CSV preview
    st.subheader("CSV Preview")
    df = pd.read_csv(uploaded_file)
    st.write(df)

def extract_text_from_docx(uploaded_file):
    try:
        document = Document(uploaded_file)
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from .doc(x) file: {e}")
        return None

def convert_docx_to_html(docx_content):
    try:
        # Convert docx content to HTML using mammoth
        result = mammoth.convert_to_html(io.BytesIO(docx_content))
        return result.value
    except Exception as e:
        st.error(f"Error converting .docx to HTML: {e}")
        return None

def show_doc(uploaded_file):
    # Display content of .doc files
    st.subheader("Document Preview")
    text = extract_text_from_docx(uploaded_file)
    if text:
        st.write(text)
    else:
        st.error("Uploaded file is not a valid Word document.")

def show_docx(uploaded_file):
    # Display content of .docx files
    st.subheader("Document Preview")
    file_name = uploaded_file.name.lower()

    if 'docx' in file_name:
        # Read the content of the uploaded file
        docx_content = uploaded_file.getvalue()

        # For .docx files, convert to HTML for preview
        html_result = convert_docx_to_html(docx_content)
        if html_result:
            st.markdown(html_result, unsafe_allow_html=True)  # Display HTML content
        else:
            st.error("Failed to convert .docx to HTML")

def show_excel(uploaded_file):
    # Display Excel preview
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("Excel Preview")
        st.write(df)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")

def show_html(uploaded_file):
    st.subheader("HTML Preview")
    html_content = uploaded_file.getvalue().decode("utf-8")
    st.markdown(html_content, unsafe_allow_html=True)

def show_md(uploaded_file):
    # Display Markdown preview
    st.subheader("Markdown Preview")
    md_content = uploaded_file.getvalue().decode("utf-8")
    st.markdown(md_content)

def show_pdf(uploaded_file):
    # Display PDF preview
    st.subheader("PDF Preview")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(uploaded_file.read()).decode("utf-8")}" width="100%" height="500"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def show_text(uploaded_file):
    #Display Text preview
    text = uploaded_file.getvalue().decode("utf-8")
    st.subheader("Text Preview")
    st.write(text)

def show_audio(uploaded_file):
    st.subheader("Audio Preview")
    audio_bytes = uploaded_file.getvalue()
    st.audio(audio_bytes, format='audio/mp3')

def show_video(uploaded_file):
    st.subheader("Video Preview")
    video_bytes = uploaded_file.getvalue()
    st.video(video_bytes)

def process_uploaded_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    print(file_name)
    file_extension = file_name.split(".")[-1]
    print(file_extension)
    file_contents = None

    if file_extension == "csv":
        show_csv(uploaded_file)
        file_contents = uploaded_file.getvalue()

    elif file_extension == "doc":
        show_doc(uploaded_file)
        doc_content = extract_text_from_docx(uploaded_file)
        file_contents = doc_content.encode("utf-8") if doc_content else None

    elif file_extension == "docx":
        show_docx(uploaded_file)
        docx_content = extract_text_from_docx(uploaded_file)
        file_contents = docx_content.encode("utf-8") if docx_content else None

    elif file_extension in ["htm", "html"]:
        show_html(uploaded_file)
        html_content = uploaded_file.getvalue().decode("utf-8")
        file_contents = html_content.encode("utf-8") if html_content else None

    elif file_extension == "md":
        show_md(uploaded_file)
        md_content = uploaded_file.getvalue().decode("utf-8")
        file_contents = md_content.encode("utf-8") if md_content else None

    elif file_extension == "pdf":
        show_pdf(uploaded_file)
        file_contents = uploaded_file.getvalue()

    elif file_extension == "txt":
        show_text(uploaded_file)
        file_contents = uploaded_file.getvalue()

    elif file_extension in ["xls", "xlsx"]:
        show_excel(uploaded_file)
        file_contents = uploaded_file.getvalue()

    elif file_extension in ["mp3"]:
        show_audio(uploaded_file)
        file_contents = uploaded_file.getvalue()

    elif file_extension in ["mp4"]:
        show_video(uploaded_file)
        file_contents = uploaded_file.getvalue()

    else:
        # Unsupported file type
        st.error("Preview not available for this file type.")

    return file_contents


with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="api_key", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 File Q&A with Anthropic")
uploaded_file = st.file_uploader("Upload an article") #, type=("txt","md")

if uploaded_file:
    file_contents = process_uploaded_file(uploaded_file)

with st.form('chat_input_form'):
    # Create two columns; adjust the ratio to your liking
    col1, col2 = st.columns([3,1]) 

    # Use the first column for text input
    with col1:
        question = st.text_input(
            "Ask something about the article",
            placeholder="Can you give me a short summary?",
            label_visibility='collapsed',
            disabled=not uploaded_file,
        )
    # Use the second column for the submit button
    with col2:
        submit_button = st.form_submit_button('Chat')

# question = st.text_input(
#     "Ask something about the article",
#     placeholder="Can you give me a short summary?",
#     disabled=not uploaded_file,
# )

# submit_button = st.button(label='Ask!')

if question and not anthropic_api_key:
    st.info("Please add your Anthropic API key to continue.")

if question and anthropic_api_key and submit_button :
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {file_contents}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model= "claude-v1",  # "claude-2" for Claude 2 model
        max_tokens_to_sample=100,
    )
    st.write("### Answer")
    st.write(response.completion)