from django.urls import path
from .views import process_prompt, process_image_and_prompt

urlpatterns = [
    path('api/process-prompt/', process_prompt, name='process_prompt'),
    path('api/process-image-and-prompt/', process_image_and_prompt, name='process_image_and_prompt'),]
