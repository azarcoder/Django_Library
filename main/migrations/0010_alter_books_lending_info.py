# Generated by Django 5.0.4 on 2024-05-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_books_bookcount_alter_books_lending_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='lending_info',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
