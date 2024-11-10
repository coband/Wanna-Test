from ninja import ModelSchema
from apps.books.models import Book

class BookSchema(ModelSchema):
    class Config:
        model = Book
        model_fields = ['id', 'title', 'author', 'ISBN', 'subject', 'published_year']

class BookCreateSchema(ModelSchema):
    class Config:
        model = Book
        model_fields = ['title', 'author', 'ISBN', 'subject', 'published_year']