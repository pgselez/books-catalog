from django.core.management.base import BaseCommand, CommandError
from ._parser import run
from catalog.models import Book


class Command(BaseCommand):
    help = 'Run parser data from goodreads.com'

    def handle(self, *args, **options):
        try:
            start = Book.objects.latest('goodreads_id').goodreads_id
        except:
            start = 0
        end = 10000
        run(start, end)
        self.stdout.write(
            self.style.SUCCESS('Parsing is Finished')
        )
