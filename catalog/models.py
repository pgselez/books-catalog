from django.db import models
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    description = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Character(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    aliases = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    source = models.URLField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Book(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    source = models.URLField(blank=True)
    description = models.TextField()
    origin_image = models.URLField()

    original_title = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=255, blank=True)
    edition_language = models.CharField(max_length=55, blank=True)
    literary_awards = models.TextField(blank=True)

    char = models.ManyToManyField(Character, blank=True)
    cats = models.ManyToManyField(Category)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def description_length(self):
        return len(str(self.description).split())


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    review = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.book


class Photo(models.Model):
    photo = models.ImageField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    original = models.URLField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
