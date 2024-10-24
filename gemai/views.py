import os
from PIL import Image
import google.generativeai as genai
from io import BytesIO
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Configure API key for Google Generative AI
genai.configure(api_key="AIzaSyCdV5PovxsEfTOUvatbyHeg11xI_GhJ1mQ")

def generate_response(prompt):
    """Generate a text-based response using the Gemini model."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def image_process(prompt, image_bytes):
    """Process the image (in bytes) using the Gemini Pro Vision model."""
    try:
        # Convert the byte data to an image using BytesIO and PIL
        image = Image.open(BytesIO(image_bytes))

        # Initialize the Gemini Pro Vision model
        model2 = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Generate content using both the prompt and the image
        response = model2.generate_content([prompt, image])

        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@api_view(['POST'])
def process_prompt(request):
    """API view to generate a response from a text prompt."""
    prompt = request.data.get("prompt", "")

    if not prompt:
        return Response({"error": "No prompt provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response_text = generate_response(prompt)
        return Response({"response": response_text}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from google.cloud import storage
import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from google.cloud import storage
import requests

@api_view(['POST'])
def process_image_and_prompt(request):
    """API view to process the image fetched from Firebase Storage using a prompt."""
    prompt = request.data.get("prompt", "")
    file_url = request.data.get("file_url", "")
    
    if not file_url:
        return Response({"error": "No file URL provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the image from Firebase Storage using the file URL
        image_bytes = fetch_image_from_firebase(file_url)

        if image_bytes:
            response_text = image_process(prompt, image_bytes)

            if response_text:
                return Response({"response": response_text}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to process the image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Failed to fetch the image from Firebase."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def fetch_image_from_firebase(file_url):
    """Fetches the image data from Firebase Storage using the file URL."""
    try:
        # Use requests to download the image file from the URL
        response = requests.get(file_url)
        
        if response.status_code == 200:
            return response.content  # Return image bytes
        else:
            print(f"Failed to download image from URL: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching image from Firebase URL: {e}")
        return None
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from groq import Groq
# Define your Groq API key and base URL
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

@api_view(['POST'])
def llmagroq(request):
    
    
    prompt = request.data.get("prompt", "")
    
    if not prompt:
        return Response({"error": "No prompt provided."}, status=status.HTTP_400_BAD_REQUEST)
    client = Groq(api_key="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")

    completion = client.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=0.65,
        stream=True,
        stop=None,
    )

    output = ""
    for chunk in completion:
        output += chunk.choices[0].delta.content or ""
    
    if output:
        return Response({"response": output}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to process the image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from groq import Groq
# Define your Groq API key and base URL
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

@api_view(['POST'])
def llmagroq2(request):
    prompt = request.data.get("prompt", "")
    if not prompt:
        return Response({"error": "No prompt provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
    model="gemma-7b-it",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

    output = ""
    for chunk in completion:
        output += chunk.choices[0].delta.content or ""
    
    if output:
        return Response({"response": output}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to process the image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
   
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from groq import Groq
# Define your Groq API key and base URL
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

@api_view(['POST'])
def llmagroq3(request):
    prompt = request.data.get("prompt", "")
    if not prompt:
        return Response({"error": "No prompt provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
    model="gemma2-9b-it",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=1.26,
    max_tokens=4330,
    top_p=1,
    stream=True,
    stop=None,
)

    output = ""
    for chunk in completion:
        output += chunk.choices[0].delta.content or ""
    
    if output:
        return Response({"response": output}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to process the image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
