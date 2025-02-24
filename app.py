from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *  
from utils import *

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Translation Function
def Translation_chain(input_text, languages):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=1, api_key=GOOGLE_API_KEY)
    prompt = PromptTemplate(input_variables=["text", "languages"], template=PROMPT)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    return llm_chain.run({"text": input_text, "languages": languages})

# Streamlit UI
st.set_page_config(page_title="Language Translator", page_icon="🌍", layout="wide")
st.title("🌍 AI-Powered Language Translator")

# Input Tabs
st.markdown("### 📥 Input Methods")
tabs = st.tabs(["📄 Upload PDF", "🔗 Enter URL", "✍️ Type Text"])

with tabs[0]:  # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

with tabs[1]:  # URL Input
    url = st.text_input("Enter a URL")

with tabs[2]:  # Text Input
    text = st.text_area("Enter your text", height=150)

# Determine Input Type
extracted_text = None
input_type = None

if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
    input_type = "PDF"
elif url:
    extracted_text = extract_text_from_url(url)
    input_type = "URL"
elif text:
    extracted_text = text
    input_type = "Text"

# Show Extracted Text
if extracted_text:
    st.markdown(f"### 🔍 Extracted Text from {input_type}:")
    st.text_area("Preview", extracted_text, height=200)

# Language Selection
languages = st.text_input("🌐 Enter the language pair (e.g., 'English to Spanish')", help="Specify the source and target language.")

# Translate Button
if st.button("🚀 Translate"):
    if not extracted_text or not languages:
        st.warning("⚠️ Please provide input text and specify languages.")
    else:
        with st.spinner("Translating..."):
            response = Translation_chain(input_text=extracted_text, languages=languages)
            st.success("✅ Translation Complete!")
            st.subheader("📝 Translated Text:")
            st.write(response)

            # Download Buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 Download as TXT", data=convert_to_txt(response), file_name="translated_text.txt", mime="text/plain")
            with col2:
                st.download_button("📥 Download as DOCX", data=convert_to_docx(response), file_name="translated_text.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
