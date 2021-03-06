# Generated by Django 2.2.16 on 2022-01-20 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0002_auto_20220117_0941"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="review",
            options={"verbose_name": "Отзыв", "verbose_name_plural": "ОТзыв"},
        ),
        migrations.RenameField(
            model_name="review",
            old_name="title_id",
            new_name="title",
        ),
        migrations.RenameField(
            model_name="titlegenre",
            old_name="genre_id",
            new_name="genre",
        ),
        migrations.RenameField(
            model_name="titlegenre",
            old_name="title_id",
            new_name="title",
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("author", "title"), name="unique Review"
            ),
        ),
    ]
