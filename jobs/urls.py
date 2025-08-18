from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_job, name='add_job'),
    path('list/', views.job_list, name='job_list'),
]
