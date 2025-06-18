from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from .models import Question, UserResponse, Option

Option.objects.update(is_current_selected=False)
Question.objects.update(is_answered=False)


def landing_page(request):
    questions = Question.objects.all()
    if questions.exists():
        question_count = questions.count()
        first_question_pk = questions.first().pk
        return render(request, 'quiz/landing.html', {'first_question_pk': first_question_pk, 'question_count': question_count})
    else:
        return HttpResponse("No Questions")


def question_view(request):
    questions = Question.objects.all()

    if (questions.exists()):
        question = questions.first()
        return render(request, 'quiz/question.html', {'question': question, 'questions': questions})
    else:
        return HttpResponse("No Questions")


def submit_form(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        # Access form data from request.POST dictionary

        question_id = request.POST.get('question_id')
        is_correct = request.POST.get('is_correct')
        time_spent = timedelta(seconds=int(request.POST.get('time_spent', 0)))
        times_option_changed = int(request.POST.get('times_option_changed', 0))
        confidence_rating = request.POST.get('confidence_rating')
        selected_option_id = request.POST.get('selected_option_id')

        question = get_object_or_404(Question, pk=question_id)
        options = question.options.all()

        if selected_option_id:
            selected_option = get_object_or_404(Option, pk=selected_option_id)
            options.update(is_current_selected=False)
            selected_option.is_current_selected = True
            selected_option.save()
            question.is_answered = True
        else:
            options.update(is_current_selected=False)
            question.is_answered = False
        question.save()

        user_response = UserResponse(
            question=question,
            time_spent=time_spent,
            times_option_changed=times_option_changed,
            is_correct=is_correct,
            user_confidence=confidence_rating
        )

        user_response.save()

        last = questions.last().pk
        next_question_pk = int(question_id) + 1

        if (next_question_pk <= last):
            next_question = get_object_or_404(
                Question, pk=(str(next_question_pk)))
            return render(request, 'quiz/question.html', {'question': next_question, 'questions': questions})
        else:
            return redirect('run_model')
    else:
        # Render the form template for GET requests
        return HttpResponse("Not Submitted")
