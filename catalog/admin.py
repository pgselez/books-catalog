from django.contrib import admin
from .models import *

# Register your models here.


def add_good_to_name(modeladmin, request, queryset):
    for o in queryset:
        o.name = 'GOOD! ' + o.name
        o.save()


add_good_to_name.short_description = "Добавить к названию слово GOOD!"


class BookAdminPhotoInline(admin.TabularInline):
    model = Photo


class BookAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'slug', 'edition_language', 'isbn'
    ]
    list_filter = ['edition_language', 'cats']
    search_fields = ['name', 'isbn']
    actions = [add_good_to_name]
    list_per_page = 50
    ordering = ['name']
    raw_id_fields = ['cats', 'char']
    list_editable = ['name', 'isbn']
    inlines = [BookAdminPhotoInline]


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'book', 'character']
    raw_id_fields = ['book', 'character']


admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Character)
