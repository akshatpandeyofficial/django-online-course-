"""
Task 2 — admin.py reference for the OnlineCourse app.

This registers the seven expected models:
Choices, Courses, Instructors, Learners, Lessons, Questions, Submissions.

IMPORTANT:
- Use this in the `django-online-course` repository required by the evaluator.
- Check the model class names in your models.py. Python class names are often
  singular (Choice, Course, Instructor, Learner, Lesson, Question, Submission),
  while Django Admin displays plural labels.
- If your models.py uses different class names, update the imports accordingly.
- If any model is already registered elsewhere, remove its duplicate registration.
"""
from django.contrib import admin
from .models import (
    Choice,
    Course,
    Instructor,
    Learner,
    Lesson,
    Question,
    Submission,
)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "content", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("content",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("id",)
    # Add actual Instructor fields here if your model defines them.


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username", "user__email")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course")
    search_fields = ("title",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "course", "grade")
    list_filter = ("course",)
    search_fields = ("content",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "learner", "question", "submitted_at")
    list_filter = ("submitted_at",)
    search_fields = ("learner__user__username", "question__content")
