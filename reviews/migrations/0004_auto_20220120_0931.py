# Generated by Django 2.2.16 on 2022-01-20 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0003_auto_20220120_0916"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="review_id",
            new_name="review",
        ),
    ]
