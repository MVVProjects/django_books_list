from django.db import models
from django.urls import reverse
        
class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default='John Doe')
    publishing_date = models.DateField(default='1900-01-01')
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    pages = models.PositiveSmallIntegerField()
    cover = models.CharField(max_length=200)
    language = models.CharField(max_length=20, default='English')
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

        
