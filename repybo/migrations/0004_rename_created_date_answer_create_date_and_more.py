# Generated by Django 4.2.7 on 2023-12-07 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repybo', '0003_answer_author_question_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='created_date',
            new_name='create_date',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='created_date',
            new_name='create_date',
        ),
    ]
