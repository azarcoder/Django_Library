# Generated by Django 5.0.4 on 2024-04-30 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('photo', models.ImageField(upload_to='photos/')),
            ],
        ),
    ]
