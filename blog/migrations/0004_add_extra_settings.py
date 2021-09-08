# Generated by Django 3.2.7 on 2021-09-08 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210908_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepreferences',
            name='heading',
            field=models.CharField(default='A blog of blogging blogosity.', max_length=200),
        ),
        migrations.AddField(
            model_name='sitepreferences',
            name='title',
            field=models.CharField(default='My Blog', max_length=20),
        ),
        migrations.AlterField(
            model_name='sitepreferences',
            name='sitename',
            field=models.CharField(default='My Sexy Blog', max_length=50),
        ),
    ]
