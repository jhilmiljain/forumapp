# Generated by Django 2.0.5 on 2018-06-26 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_remove_question_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Answer'),
        ),
    ]