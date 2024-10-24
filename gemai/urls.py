from django.urls import path
from .views import process_prompt, process_image_and_prompt,llmagroq

urlpatterns = [
    path('api/process-prompt/', process_prompt, name='process_prompt'),
    path('api/process-image-and-prompt/', process_image_and_prompt, name='process_image_and_prompt'),
    path('api/groq-chat-completion/', llmagroq, name='groq_chat_completion'),
    ]
