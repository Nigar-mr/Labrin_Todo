# Generated by Django 2.2.5 on 2019-09-05 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0003_myuser_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]