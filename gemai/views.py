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

@api_view(['POST'])
def process_image_and_prompt(request):
    """API view to process the image fetched from Firebase Storage using a prompt."""
    prompt = request.data.get("prompt", "")
    image_id = request.data.get("image_id", "")
    
    if not image_id:
        return Response({"error": "No image ID provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the image from Firebase Storage
        image_bytes = fetch_image_from_firebase(image_id)

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

def fetch_image_from_firebase(image_id):
    """Fetches the image data from Firebase Storage using the image ID."""
    client = storage.Client()  # Create a client
    bucket_name = 'scorewise-c3220.appspot.com'  # Replace with your Firebase Storage bucket name
    bucket = client.get_bucket(bucket_name)
    
    try:
        blob = bucket.blob(image_id)  # Use the image ID to create a blob reference
        image_data = blob.download_as_bytes()  # Download the image as bytes
        return image_data
    except Exception as e:
        print(f"Error fetching image from Firebase: {e}")
        return None
