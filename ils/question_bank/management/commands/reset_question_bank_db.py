from django.core.management.base import BaseCommand
from django.db import connection
from question_bank.models import Question


class Command(BaseCommand):
    help = 'Delete all entries in the Question model and reset the primary key sequence.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting all entries from the database...')
        Question.objects.all().delete()
        self.stdout.write('All entries deleted.')

        self.stdout.write('Resetting the primary key sequence...')
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'question_bank_question'")
            cursor.execute(
                "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'question_bank_option'")
        self.stdout.write('Primary key sequence reset.')
