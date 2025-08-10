from django.urls import path
from setuptools.extern import names

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('filter/<str:status>/', views.filter_tasks, name='filter_tasks'),
    path('profile/', views.profile, name='profile'),
    path('export/excel/', views.export_tasks_excel, name='export_excel'),
    path('export/pdf/', views.export_tasks_pdf, name='export_pdf'),
]