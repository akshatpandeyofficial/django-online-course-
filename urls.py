"""
Task 6: URL patterns for the mock exam and course detail views.

Merge these patterns into your app's existing urls.py; do not remove
other routes your project already uses.
"""
from django.urls import path
from . import views

urlpatterns = [
    path(
        "courses/<int:course_id>/",
        views.course_details,
        name="course_details",
    ),
    path(
        "mock-exam/",
        views.mock_exam,
        name="mock_exam",
    ),
    path(
        "submit-exam/",
        views.submit_exam,
        name="submit_exam",
    ),
    path(
        "exam-result/",
        views.show_exam_result,
        name="show_exam_result",
    ),
]
