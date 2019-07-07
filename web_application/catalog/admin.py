from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.


def add_good_to_name(modeladmin, request, queryset):
    for o in queryset:
        o.name = 'GOOD! ' + o.name
        o.save()


add_good_to_name.short_description = "Добавить к названию слово GOOD!"


class BookAdminPhotoInline(admin.TabularInline):
    model = Photo


class BookAdmin(SummernoteModelAdmin):
    list_display = [
        'name', 'chow_cats_count', 'show_image',
        'go_to_google', 'slug',
        'edition_language', 'isbn'
    ]
    summernote_fields = ('description', 'literary_awards')
    list_filter = ['edition_language', 'cats']
    search_fields = ['name', 'isbn']
    actions = [add_good_to_name]
    list_per_page = 50
    ordering = ['name']
    raw_id_fields = ['cats', 'char']
    list_editable = ['isbn']
    inlines = [BookAdminPhotoInline]

    def chow_cats_count(self, book):
        try:
            count = book.cats.count()
        except Exception:
            count = 'not-found'
        return count

    def show_image(self, book):
        try:
            img = mark_safe(f'<img style="max-height: 50px" src="{book.origin_image}">')
        except Exception:
            img = 'not-found'
        return img

    def go_to_google(self, book):
        try:
            base_link = 'https://google.com/search?q={}'.format(book.name)
            link = mark_safe(f'<a href="{base_link}" target="_blank">go to google</a>')
        except Exception:
            link = 'not-found'
        return link

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.defer('literary_awards', 'original_title', 'description')
        qs = qs.prefetch_related('cats', 'char')
        return qs


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'book', 'character']
    raw_id_fields = ['book', 'character']


admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Character)
