from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_job, name='add_job'),
    path('jobs/', views.job_list, name='job_list'),  # only one route for list
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('jobs/<int:job_id>/applications/', views.view_applications, name='view_applications'),
]
