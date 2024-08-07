# Generated by Django 5.0.6 on 2024-07-06 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hintBase', '0007_alter_problem_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_rating', models.FloatField(blank=True, default=0, null=True)),
                ('ratings', models.JSONField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hintBase.problem')),
            ],
        ),
    ]
