# Generated by Django 5.0.6 on 2024-06-22 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hintBase', '0005_problem_date_problem_time_problemhint_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
