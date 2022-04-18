import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


def get_valid_csv_row(row):
    if row.get("id"):
        row["id"] = int(row["id"])
    if row.get("category"):
        row["category"] = Category.objects.get(pk=int(row["category"]))
    if row.get("title_id"):
        row["title"] = Title.objects.get(pk=int(row["title_id"]))
    if row.get("genre_id"):
        row["genre"] = Genre.objects.get(pk=int(row["genre_id"]))
    if row.get("author"):
        row["author"] = User.objects.get(pk=int(row["author"]))
    if row.get("review_id"):
        row["review"] = Review.objects.get(pk=int(row["review_id"]))
    return row


class Command(BaseCommand):
    help = "import base data"

    def handle(self, *args, **options):
        def import_csv(self, files, model):
            print(f"start import {files}")
            try:
                with open(files) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        _, created = model.objects.get_or_create(
                            **get_valid_csv_row(row)
                        )
            except Exception as e:
                print(f"ошибка при загрузке файла {e}")
            print(f"finish import {files}")

        import_csv(self, "./static/data/users.csv", User)
        import_csv(self, "./static/data/genre.csv", Genre)
        import_csv(self, "./static/data/category.csv", Category)
        import_csv(self, "./static/data/titles.csv", Title)
        import_csv(self, "./static/data/genre_title.csv", TitleGenre)
        import_csv(self, "./static/data/review.csv", Review)
        import_csv(self, "./static/data/comments.csv", Comment)
