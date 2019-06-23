from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    cats = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    review = models.TextField()

    def __str__(self):
        return self.book
