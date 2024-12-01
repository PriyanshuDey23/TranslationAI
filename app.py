from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *  
from utils import  *


# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Response Format For Language Translation
def Translation_chain(input_text, languages):
    # Define the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=1, api_key=GOOGLE_API_KEY)  
    
    # Define the prompt
    PROMPT_TEMPLATE = PROMPT  # Imported from prompt.py, should contain a translation prompt
    prompt = PromptTemplate(
            input_variables=["text", "languages"],  
            template=PROMPT_TEMPLATE,
        )
      
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate response
    response = llm_chain.run({"text": input_text, "languages": languages})
    return response

# Consolidated input handling function
def get_input_data():

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    url = st.text_input("Enter a URL")
    text = st.text_area("Enter your text", height=200)

    # Handle PDF input
    if uploaded_file:
        extracted_text = extract_text_from_pdf(uploaded_file)
        input_type = "PDF"
    # Handle URL input
    elif url:
        extracted_text = extract_text_from_url(url)
        input_type = "URL"
    # Handle direct text input
    elif text:
        extracted_text = text
        input_type = "Text"
    else:
        extracted_text = None
        input_type = None

    return extracted_text, input_type


# Streamlit app
st.set_page_config(page_title="Language Translator")
st.header("Language Translator")

# Get user input (file, URL, or direct text)
user_input, input_type = get_input_data()

# Display extracted or entered text
if user_input:
    st.text_area(f"Extracted Text from {input_type}", user_input, height=200)
# Input language specification 
languages = st.text_input("Enter the language pair (e.g., 'English to Spanish')")

# Translate button
if st.button("Translate"):
    response = Translation_chain(input_text=user_input, languages=languages)
    st.subheader("The Translation is:")
    st.write(response)

    # Download options
    st.download_button(
            label="Download as TXT",
            data=convert_to_txt(response),
            file_name="translated_text.txt",
            mime="text/plain",
        )
    st.download_button(
            label="Download as DOCX",
            data=convert_to_docx(response),
            file_name="translated_text.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

