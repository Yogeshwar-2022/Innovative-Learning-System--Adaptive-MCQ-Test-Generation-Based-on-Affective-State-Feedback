# Generated by Django 3.0.5 on 2024-03-11 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20240309_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='cognitive_ability',
            field=models.CharField(choices=[('Level_1', 'Remember and Understand'), ('Level_2', 'Apply and Analyze'), ('Level_3', 'Evaluate and Create')], max_length=50),
        ),
        migrations.AlterField(
            model_name='question',
            name='label',
            field=models.CharField(max_length=5000),
        ),
    ]
