import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name="Категория")
    slug = models.SlugField(max_length=10, verbose_name="slug", unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=20, verbose_name="Название произведения"
    )
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.date.today().year),
        ],
        verbose_name="Год",
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="category_title",
        verbose_name="Категория",
    )
    description = models.TextField(default="")
    genre = models.ManyToManyField(
        Genre, default=None, related_name="genre", blank=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveIntegerField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Отзыв"
        verbose_name_plural = "ОТзыв"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique Review"
            )
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.text[:10]


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
