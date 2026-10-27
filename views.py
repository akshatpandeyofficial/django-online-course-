"""
Task 5 reference views for the Django OnlineCourse project.

This file provides the required submit_exam and show_exam_result views.
IMPORTANT: integrate these functions into your actual project's views.py and
adapt model/field names to the models.py in your django-online-course repository.
The sample assumes:
  Question(question_text), related manager `choices`
  Choice(choice_text, is_correct)
  Submission(user, question, choice, is_correct)
  Course/Lesson models are handled separately by course views.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Question, Submission


@login_required
def mock_exam(request):
    """Render the quiz form."""
    questions = Question.objects.prefetch_related("choices").all()
    return render(request, "exam.html", {"questions": questions})


@login_required
@require_POST
def submit_exam(request):
    """Save each answer, calculate the score, and redirect to the results page."""
    questions = list(Question.objects.prefetch_related("choices").all())
    total_questions = len(questions)
    score = 0
    result_rows = []

    for question in questions:
        posted_choice_id = request.POST.get(f"question_{question.pk}")
        selected_choice = (
            question.choices.filter(pk=posted_choice_id).first()
            if posted_choice_id
            else None
        )
        is_correct = bool(selected_choice and selected_choice.is_correct)
        score += int(is_correct)

        # Adapt these fields if your Submission model uses a different schema.
        Submission.objects.create(
            user=request.user,
            question=question,
            choice=selected_choice,
            is_correct=is_correct,
        )

        result_rows.append({
            "question_id": question.pk,
            "selected_choice_id": selected_choice.pk if selected_choice else None,
            "is_correct": is_correct,
        })

    percentage = round(score * 100 / total_questions, 2) if total_questions else 0
    passed = percentage >= 70

    request.session["mock_exam_summary"] = {
        "score": score,
        "total": total_questions,
        "percentage": percentage,
        "passed": passed,
    }
    request.session["mock_exam_results"] = result_rows

    return redirect("show_exam_result")


@login_required
def show_exam_result(request):
    """Display the congratulations/status message, score, and answer-by-answer review."""
    summary = request.session.get("mock_exam_summary")
    saved_results = request.session.get("mock_exam_results", [])

    if summary is None:
        messages.info(request, "Please complete and submit the mock exam first.")
        return redirect("mock_exam")

    question_ids = [row["question_id"] for row in saved_results]
    questions = Question.objects.filter(pk__in=question_ids).prefetch_related("choices")
    questions_by_id = {question.pk: question for question in questions}

    result_by_id = {row["question_id"]: row for row in saved_results}
    results = []

    # Keep the same order as the submitted exam.
    for question_id in question_ids:
        question = questions_by_id.get(question_id)
        if question is None:
            continue

        saved_row = result_by_id[question_id]
        selected_id = saved_row["selected_choice_id"]
        selected_choice = (
            question.choices.filter(pk=selected_id).first()
            if selected_id
            else None
        )
        correct_choice = question.choices.filter(is_correct=True).first()

        results.append({
            "question": question,
            "selected_choice": selected_choice,
            "correct_choice": correct_choice,
            "is_correct": bool(selected_choice and selected_choice.is_correct),
        })

    return render(request, "exam_result.html", {
        "summary": summary,
        "results": results,
    })
