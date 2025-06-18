# question_bank/management/commands/select_questions.py

from django.core.management.base import BaseCommand
from exam.models import Question as ExamQuestion, Option as ExamOption
from question_bank.models import Question as QuestionBankQuestion


class Command(BaseCommand):
    help = 'Select questions from question bank based on A value and transfer them to exam'

    def add_arguments(self, parser):
        parser.add_argument('A', type=float, help='The value of A')

    def handle(self, *args, **options):
        A = options['A']
        self.stdout.write(
            'selecting questions from question bank based on A value...')
        selected_questions = self.select_questions_from_question_bank(A)
        self.stdout.write('questions selected')
        self.stdout.write('transferring questions to exam database...')
        self.transfer_questions_to_exam(selected_questions)
        self.stdout.write('transfer completed')

    def select_questions_from_question_bank(self, A):
        # Define the mapping of affective state value to ratio of level-wise questions
        # This is based on the provided table
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

        return selected_questions

    def transfer_questions_to_exam(self, selected_questions):
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
