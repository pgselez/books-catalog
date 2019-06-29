from django.db import models
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    description = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Book(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    description = models.TextField()
    drive_image = models.ImageField(blank=True)
    origin_image = models.URLField()
    cats = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    review = models.TextField()

    def __str__(self):
        return self.book
