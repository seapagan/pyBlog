# Generated by Django 3.2.9 on 2021-11-14 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='guest_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]