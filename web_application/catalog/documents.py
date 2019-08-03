from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Book, Author


@registry.register_document
class BookIndex(Document):
    class Index:
        name = 'books'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Book

        fields = [
            'name',
            'description',
            'goodreads_id',
            'id',
            'isbn',
            'original_title',
            'edition_language',
            'literary_awards'
        ]


@registry.register_document
class AuthorIndex(Document):
    class Index:
        name = 'authors'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Author

        fields = [
            'name',
            'biography',
            'id'
        ]
