# Generated by Django 3.2.3 on 2021-05-20 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_question_question_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionsupdate',
            name='file_description',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AddField(
            model_name='questionsupdate',
            name='file_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
