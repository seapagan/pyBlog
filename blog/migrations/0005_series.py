# Generated by Django 3.2.13 on 2022-05-01 09:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0004_auto_20220207_1650"),
    ]

    operations = [
        migrations.CreateModel(
            name="Series",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("series_name", models.CharField(max_length=50)),
                ("slug", models.SlugField(default="", unique=True)),
                ("posts", models.ManyToManyField(blank=True, to="blog.Blog")),
                (
                    "series_creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="series",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]