from django.urls import path
from .views import process_prompt, process_image_and_prompt,llmagroq,llmagroq2,llmagroq3

urlpatterns = [
    path('api/process-prompt/', process_prompt, name='process_prompt'),
    path('api/process-image-and-prompt/', process_image_and_prompt, name='process_image_and_prompt'),
    path('api/groq-chat-completion/', llmagroq, name='groq_chat_completion'),
    path('api/groq-chat-completion2/', llmagroq2, name='groq_chat_completion2'),
    path('api/groq-chat-completion3/', llmagroq3, name='groq_chat_completion3'),
    ]
