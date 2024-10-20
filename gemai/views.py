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

@api_view(['POST'])
def process_image_and_prompt(request):
    """API view to process the uploaded image and generate a response using a prompt."""
    prompt = request.data.get("prompt", "")
    image_file = request.FILES.get("image")

    if not image_file:
        return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Read the image file as byte content
        image_bytes = image_file.read()
        response_text = image_process(prompt, image_bytes)

        if response_text:
            return Response({"response": response_text}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to process the image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
