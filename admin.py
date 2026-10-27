from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Enrollment,
    Question,
    Choice,
    Submission,
)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "lesson", "grade")
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    inlines = [QuestionInline]


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [LessonInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
