from .models import Book
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = [
            'name', 'source', 'isbn', 'edition_language',
            'description', 'literary_awards'
        ]


# ViewSets define the view behavior.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
