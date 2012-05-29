from records.models import Book

def get_books(scope, query):
    if scope == 'T':
        books = Book.objects.filter(name__icontains=query)
    elif scope == 'A':
        books = Book.objects.filter(authors__icontains=query)
    elif scope == 'I':
        books = Book.objects.filter(isbn=query)
    else:
        books = Book.objects.filter(name__icontains='')
    return books
