# Generated by Django 3.2.1 on 2021-05-07 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_group',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(default='', max_length=2000),
        ),
    ]
