import os
from io import BytesIO

import openai
import PyPDF2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = os.getenv("OPENAI_BASE_URL")

def read_pdf(file):
    """
    Read the text content from a PDF file.

    Args:
        file (str): The path to the PDF file.

    Returns:
        str: The extracted text content from the PDF file.
    """
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_response(prompt, model=os.getenv("OPENAI_MODEL")):
    """
    Generates a response using the OpenAI chat completions API.

    Args:
        prompt (str): The user's prompt or message.
        model (str, optional): The name or ID of the OpenAI model to use. Defaults to the value of the OPENAI_MODEL environment variable.

    Returns:
        str: The generated response.

    Raises:
        OpenAIError: If there is an error with the OpenAI API request.
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def main():
    """
    This function is the main entry point of the application.
    It allows users to upload a resume, enter job details, and generate various communication messages based on the resume content and job details.
    Users can also have a chat-like interaction with the assistant to ask questions about their resume.
    """
    st.title("Resume to Communication Tool")

    uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        resume_text = read_pdf(BytesIO(file_bytes))

        job_description = st.text_input("Enter the job description:")
        role_title = st.text_input("Enter the role title:")
        company_name = st.text_input("Enter the company name:")

        st.subheader("LinkedIn Cold DM")
        st.text(generate_response(f"Generate a LinkedIn cold DM for a recruiter based on the following resume content and job details:\nResume Content: {resume_text}\nJob Description: {job_description}\nRole Title: {role_title}\nCompany Name: {company_name}"))

        st.subheader("Cold Email")
        st.text(generate_response(f"Generate a cold email to get hired at a company based on the following resume content and job details:\nResume Content: {resume_text}\nJob Description: {job_description}\nRole Title: {role_title}\nCompany Name: {company_name}"))

        st.subheader("Twitter DM")
        st.text(generate_response(f"Generate a Twitter DM to a recruiter based on the following resume content and job details:\nResume Content: {resume_text}\nJob Description: {job_description}\nRole Title: {role_title}\nCompany Name: {company_name}"))

        st.subheader("Twitter Post")
        st.text(generate_response(f"Generate a Twitter post to promote your skills and experience based on the following resume content and job details:\nResume Content: {resume_text}\nJob Description: {job_description}\nRole Title: {role_title}\nCompany Name: {company_name}"))

        st.subheader("Chat with Document")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask something about your resume:"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = generate_response(f"Based on the following resume content, {prompt}: {resume_text}")
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == '__main__':
    main()