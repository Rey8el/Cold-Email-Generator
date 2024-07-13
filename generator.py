import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please generate a cold email based on the following information."),
        ("user", "Personal Info: {personal_info}\nJob Description (optional): {job_description}\nCompany Info: {company_info}")
    ]
)

llm = Ollama(model="llama2")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Streamlit framework
st.title('Cold Email Generator')

# Serve HTML file
html_file = open('user_input.html', 'r').read()
st.markdown(html_file, unsafe_allow_html=True)

# Capture form submission
personal_info = st.text_input("Enter your personal info (hidden)")
job_description = st.text_input("Enter the job description (hidden)")
company_info = st.text_input("Enter the company info (hidden)")

if st.button("Generate Cold Email"):
    if personal_info and company_info:
        result = chain.invoke({
            "personal_info": personal_info,
            "job_description": job_description,
            "company_info": company_info
        })
        st.write(result)
    else:
        st.warning("Please provide at least your personal info and company info.")
