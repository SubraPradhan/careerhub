from django.test import TestCase

# Create your tests here.
from django.urls import path
from . import views

urlpatterns = [
    # other urls
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
]
