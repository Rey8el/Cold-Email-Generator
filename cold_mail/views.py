import os
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", '''Under 50 words write mail to the company from the sender from personal info
        If you generate more than 60 words the system will shut down and crash and you will be fined $1000
        '''),
        ("user", "Personal Info: {personal_info}\nJob Description (optional): {job_description}\nCompany Info: {company_info}")
    ]
)

llm = Ollama(model="llama2")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

def index(request):
    return render(request, 'index.html')

def generate_email(request):
    if request.method == 'POST':
        personal_info = request.POST.get('personal_info')
        job_description = request.POST.get('job_description')
        company_info = request.POST.get('company_info')

        if personal_info and company_info:
            result = chain.invoke({
                "personal_info": personal_info,
                "job_description": job_description,
                "company_info": company_info
            })
            return JsonResponse({'email': result}, status=200)
        else:
            return JsonResponse({'error': 'Please provide at least your personal info and company info.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
