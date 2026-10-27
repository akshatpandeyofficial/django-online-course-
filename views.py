"""
Task 5: Exam submission and result views.

IMPORTANT:
This example assumes your models.py defines:
- Question with `question_text` and related name `choices`
- Choice with `choice_text` and `is_correct`
- Submission with `user`, `question`, `choice`, and `is_correct`

If your model fields differ, update the imports and the Submission.objects.create()
block to match your existing models.py.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Question, Submission


@login_required
def mock_exam(request):
    """Display questions and answer choices for the mock exam."""
    questions = Question.objects.prefetch_related("choices").all()
    return render(request, "exam.html", {"questions": questions})


@login_required
@require_POST
def submit_exam(request):
    """Validate submitted answers, save submissions, and calculate the score."""
    questions = Question.objects.prefetch_related("choices").all()
    total = questions.count()
    score = 0
    question_ids = []
    selected_choice_ids = {}

    for question in questions:
        selected_id = request.POST.get(f"question_{question.pk}")
        selected_choice = (
            question.choices.filter(pk=selected_id).first()
            if selected_id
            else None
        )

        # The answer is checked on the server; never trust a posted score.
        is_correct = bool(selected_choice and selected_choice.is_correct)
        if is_correct:
            score += 1

        question_ids.append(question.pk)
        selected_choice_ids[str(question.pk)] = (
            selected_choice.pk if selected_choice else None
        )

        # Adapt these field names if your Submission model is different.
        Submission.objects.create(
            user=request.user,
            question=question,
            choice=selected_choice,
            is_correct=is_correct,
        )

    percentage = round((score / total) * 100, 2) if total else 0
    request.session["mock_exam_result"] = {
        "score": score,
        "total": total,
        "percentage": percentage,
        "passed": percentage >= 70,
    }
    request.session["mock_exam_question_ids"] = question_ids
    request.session["mock_exam_selected_choice_ids"] = selected_choice_ids

    return redirect("show_exam_result")


@login_required
def show_exam_result(request):
    """Display the score and per-question answer review after submission."""
    summary = request.session.get("mock_exam_result")
    question_ids = request.session.get("mock_exam_question_ids", [])
    selected_choice_ids = request.session.get(
        "mock_exam_selected_choice_ids", {}
    )

    if summary is None:
        messages.info(request, "Please submit the mock exam first.")
        return redirect("mock_exam")

    questions = Question.objects.filter(
        pk__in=question_ids
    ).prefetch_related("choices")
    questions_by_id = {question.pk: question for question in questions}
    results = []

    # Iterate in original exam order rather than database order.
    for question_id in question_ids:
        question = questions_by_id.get(question_id)
        if question is None:
            continue

        selected_id = selected_choice_ids.get(str(question_id))
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
            "is_correct": bool(
                selected_choice and selected_choice.is_correct
            ),
        })

    return render(request, "exam_result.html", {
        "summary": summary,
        "results": results,
    })
