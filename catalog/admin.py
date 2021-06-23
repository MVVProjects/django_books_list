from django.contrib import admin
from .models import Book

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publishing_date', 'language',
                    'isbn', 'cover', 'pages')
    list_filter = ('title', 'author', 'language', 'publishing_date')

