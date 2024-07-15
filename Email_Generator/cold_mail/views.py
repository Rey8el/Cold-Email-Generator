import os
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Ensure the functions are defined correctly within the appropriate views
def index(request):
    return render(request, 'index.html')

def generate_email(request):
    if request.method == 'POST':
        personal_info = request.POST.get('personal_info')
        job_description = request.POST.get('job_description')
        company_info = request.POST.get('company_info')

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        input_prompt = """
        Hey, act like a skilled and highly experienced Cold Email Generator with a deep understanding of various professional fields, including but not limited to tech, healthcare, finance, education, marketing, and more. Your task is to generate a 50-word email based on the given job description.

        Consider that the job market is very competitive, and you should provide the best assistance for generating a cold email. Analyze the job description and company description:

        1. Generate a 50-word impactful cold email based on the summary of the job description.

        Please provide your analysis with high accuracy, considering relevant experience, and any specific requirements mentioned in the job description and align with the company description.

        Based on your analysis, please provide:
        A generative 50-word cold email template suitable for the job description and aligns with the company.
        """

        system_settings = [
            {
                "role": "system",
                "content": input_prompt
            },
            {
                "role": "user",
                "content": f"company Info = {company_info}, Job Description = {job_description}",
            }
        ]

        response = client.chat.completions.create(
            messages=system_settings,
            model="llama3-8b-8192",
            temperature=0.5,
            top_p=1,
            stop=None,
            stream=False,
        )

        email_content = response.choices[0].message.content
        return JsonResponse({"email": email_content})

    return JsonResponse({"error": "Invalid request method."})

