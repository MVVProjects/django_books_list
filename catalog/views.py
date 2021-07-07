import datetime
import requests
import json
import dateutil.parser as dparser

from .models import Book
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpRequest
from django.urls import reverse, reverse_lazy
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.serializers import BookSerializer

class BookListView(generic.ListView):
    model = Book.objects.all().order_by('id')
    paginate_by = 10
    
class BookDetailView(generic.DetailView):
    model = Book.objects.all().order_by('id')
       
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    context = {'num_books': num_books,}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'publishing_date', 'isbn',
              'pages', 'cover', 'language']

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'publishing_date', 'isbn',
              'pages', 'cover', 'language']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or filtered.
    """
    model = Book
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('title')
    
class BooksList(APIView):
    """List all books."""
    objects = Book._default_manager
    def get(self, request, format=None):
        books = Book.objects.all().order_by('title')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, safe=False)
        
def get_books(request):
    """Import books via API with search button"""
    all_books = {}
    if 'name' in request.GET:
        name = request.GET['name']
        url = 'https://www.googleapis.com/books/v1/volumes?q=%s' % name
        response = requests.get(url)
        data = response.json()
        books = data['items']
        
        for i in range(len(books)):
            try:
                book_data = Book(
                    title = books[i]['volumeInfo']['title'],
                    author = books[i]['volumeInfo']['authors'],
                    publishing_date = dparser.parse((books[i]['volumeInfo']
                                      ['publishedDate']),fuzzy=True).date(),
                    isbn = books[i]['volumeInfo']['industryIdentifiers']
                                [1]['identifier'],
                    pages = books[i]['volumeInfo']['pageCount'],
                    cover = books[i]['volumeInfo']['imageLinks']['thumbnail'],
                    language = books[i]['volumeInfo']['language'],
                )
            except:
                continue
            book_data.save()
            all_books = Book.objects.all().order_by('-id')
    return render(request, 'catalog/book_search.html', {"all_books": all_books},)
