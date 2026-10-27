"""
Task 6: URL patterns for the django-online-course project.

Merge these routes into the project's actual app-level urls.py.
The required routes are submit_exam and show_exam_result.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("submit-exam/", views.submit_exam, name="submit_exam"),
    path("exam-result/", views.show_exam_result, name="show_exam_result"),
    path("mock-exam/", views.mock_exam, name="mock_exam"),
]
