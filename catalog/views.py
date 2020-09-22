from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre


def index(request):
    count_books = Book.objects.count()
    count_instances = BookInstance.objects.count()
    count_instances_available = BookInstance.objects.filter(status__exact="a").count()
    count_authors = Author.objects.count()

    return render(
        request,
        'index.html',
        context={
            'count_books': count_books,
            'count_instances': count_instances,
            'count_instances_available': count_instances_available,
            'count_authors': count_authors
        }
    )


class BookList(generic.ListView):
    model = Book
    template_name = 'books.html'

    def get_queryset(self):
        return Book.objects.all()[:10]


class BookInfo(generic.DetailView):
    model = Book
    template_name = 'book-info.html'

