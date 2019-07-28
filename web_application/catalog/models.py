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

    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    link = models.URLField(max_length=255)
    photo_origin = models.URLField(max_length=255, null=True)
    photo = models.ImageField(blank=True, upload_to='authors', null=True)
    biography = models.TextField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Book(models.Model):
    name = models.CharField(max_length=255)
    goodreads_id = models.IntegerField()
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    source = models.URLField(blank=True)
    description = models.TextField(blank=True)
    origin_image = models.URLField(blank=True)

    owner = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)

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
    publish = models.BooleanField(default=False)
    nickname = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    review = models.TextField()
    data = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.book.name


class Photo(models.Model):
    photo = models.ImageField(blank=True, upload_to='photos')
    name = models.CharField(max_length=255, blank=True)
    original = models.URLField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
