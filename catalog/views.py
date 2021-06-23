import datetime, requests
import json

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book
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
    model = Book.objects.get_queryset().order_by('id')
    paginate_by = 10
    
class BookDetailView(generic.DetailView):
    model = Book.objects.get_queryset().order_by('id')
       
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
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BooksList(APIView):
    """List all books."""
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, safe=False)
