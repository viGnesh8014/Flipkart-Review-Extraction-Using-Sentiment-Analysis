# Generated by Django 5.0.3 on 2024-03-26 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0003_review_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='review_result',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]