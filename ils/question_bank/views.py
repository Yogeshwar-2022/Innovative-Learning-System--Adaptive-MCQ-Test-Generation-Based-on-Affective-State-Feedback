from django.shortcuts import render, redirect

from quiz.models import Question as QuizQuestion, UserResponse as QuizUserResponse
from exam.models import Question as ExamQuestion, Option as ExamOption
from question_bank.models import Question as QuestionBankQuestion

import pandas as pd
import numpy as np
from math import floor
from sklearn.ensemble import RandomForestRegressor
import joblib
from django.db import connection

# Create your views here.


def run_model(request):
    # Load user response data
    user_responses = QuizUserResponse.objects.all()
    user_responses_list = list(user_responses.values())
    df_userresponse = pd.DataFrame(user_responses_list)

    df_userresponse['time_spent'] = df_userresponse['time_spent'].apply(
        lambda x: x.total_seconds())

    # Aggregate user response data
    df_userresponse = df_userresponse.groupby('question_id').agg({
        'id': 'last',
        'times_option_changed': 'sum',
        'is_correct': 'last',
        'user_confidence': lambda x: floor(x.mean()),
        'time_spent': 'sum'
    }).reset_index()

    df_userresponse = df_userresponse[[
        'id', 'times_option_changed', 'is_correct', 'question_id', 'user_confidence', 'time_spent']]

    # Load question data
    quiz_question = QuizQuestion.objects.all()
    quiz_question_list = list(quiz_question.values())
    df_question = pd.DataFrame(quiz_question_list)

    # Map cognitive ability to user responses
    question_cognitive_ability = dict(
        zip(df_question['id'], df_question['cognitive_ability']))
    df_userresponse['cognitive_ability'] = df_userresponse['question_id'].map(
        question_cognitive_ability)

    # Normalize time spent and map cognitive ability levels
    df_userresponse['time_spent'] = df_userresponse['time_spent'].apply(
        lambda x: x / 1000000)
    cognitive_ability_mapping = {'Level_1': 1, 'Level_2': 2, 'Level_3': 3}
    df_userresponse['cognitive_ability'] = df_userresponse['cognitive_ability'].map(
        cognitive_ability_mapping)

    # Define features and target
    features = ['time_spent', 'times_option_changed',
                'is_correct', 'cognitive_ability']
    target = 'user_confidence'

    X = df_userresponse[features]
    y = df_userresponse[target]

    # Train the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save the trained model
    joblib.dump(model, 'confidence_predictor_model.pkl')
    A = floor(df_userresponse['user_confidence'].mean())

    question_ratio_mapping = {
        (1): (15, 0, 0),
        (2): (13, 2, 0),
        (3): (10, 5, 0),
        (4): (7, 7, 1),
        (5): (5, 8, 2),
        (6): (3, 10, 2),
        (7): (2, 8, 5),
        (8): (2, 5, 8),
        (9): (1, 3, 11),
        (10): (0, 0, 15)
    }

    # Find the range of A and get the corresponding ratio
    selected_ratio = None
    for value in question_ratio_mapping.keys():
        if A == value:
            selected_ratio = question_ratio_mapping[(value)]
            break

    if selected_ratio is None:
        raise ValueError("Invalid value of A")

    # Select questions from the question bank based on the ratio
    selected_questions = []
    for level, count in enumerate(selected_ratio, start=1):
        questions = QuestionBankQuestion.objects.filter(
            cognitive_ability=f'Level_{level}')[:count]
        selected_questions.extend(questions)

    ExamQuestion.objects.all().delete()

    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'exam_question'")
        cursor.execute(
            "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'exam_option'")
        cursor.execute(
            "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'exam_userresponse'")

    for question in selected_questions:
        # Create a new question in the exam database
        exam_question = ExamQuestion.objects.create(
            label=question.label,
            cognitive_ability=question.cognitive_ability
        )

        # Transfer options for the question
        for option in question.options.all():
            ExamOption.objects.create(
                question=exam_question,
                text=option.text,
                is_correct=option.is_correct
            )

    return redirect('exam_landing_page')
