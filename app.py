from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *  


# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Response Format For Language Translation
def Translation_chain(input_text, languages):
    # Define the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002", temperature=1, api_key=GOOGLE_API_KEY)  
    
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


# Streamlit app
st.set_page_config(page_title="Language Translator")
st.header("Language Translator")

# Input text
text = st.text_area("Enter the text you want to translate (e.g., 'Translate from English to French: ')", height=200)

# Input language specification 
languages = st.text_input("Enter the language pair (e.g., 'English to Spanish')")

# Translate button
if st.button("Translate"):
    if text and languages:
        response = Translation_chain(input_text=text, languages=languages)
        st.write("The Translation is: \n\n", response)
    else:
        st.warning("Please enter both the text to translate and the language pair.")
