# Generated by Django 2.0.5 on 2018-06-27 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20180626_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='answer_text',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='forum.Answer'),
            preserve_default=False,
        ),
    ]