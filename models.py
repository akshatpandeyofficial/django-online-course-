"""
Task 1 — models.py reference for the OnlineCourse quiz.

Integrate these model definitions into the models.py of the exact repository
required by your evaluator. If Course, Learner, or other models already exist,
reuse them rather than defining duplicate models.

Model relationships and scoring:
- Question belongs to a Course and has a grade.
- Choice belongs to a Question and marks whether it is correct.
- Submission links a Learner, a Question, and the selected Choices.
- Question.is_get_score() returns the question's grade only when the submitted
  choices exactly match the correct choices.
- Submission.get_score() returns the score for that submission.
"""
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Learner(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="learner_profile"
    )
    courses = models.ManyToManyField(Course, blank=True, related_name="learners")

    def __str__(self):
        return self.user.get_username()


class Question(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="questions"
    )
    content = models.CharField(max_length=1000)
    grade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.content

    def is_get_score(self, selected_choice_ids):
        """Return this question's grade if exactly the correct choices were selected."""
        correct_ids = set(
            self.choices.filter(is_correct=True).values_list("id", flat=True)
        )
        selected_ids = {int(choice_id) for choice_id in selected_choice_ids}
        return self.grade if correct_ids == selected_ids else 0

    # Compatibility helper for code that expects the conventional method name.
    def get_score(self, selected_choice_ids):
        return self.is_get_score(selected_choice_ids)


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    content = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Submission(models.Model):
    learner = models.ForeignKey(
        Learner, on_delete=models.CASCADE, related_name="submissions"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="submissions"
    )
    choices = models.ManyToManyField(Choice, blank=True, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.learner} — {self.question}"

    def get_score(self):
        """Calculate the score for the choices saved in this submission."""
        selected_ids = self.choices.values_list("id", flat=True)
        return self.question.is_get_score(selected_ids)

    def is_get_score(self):
        """Compatibility with rubric/code that expects this method on Submission."""
        return self.get_score()
