from ninja import ModelSchema, Schema
from apps.books.models import Book
from datetime import date

class BookSchema(ModelSchema):
  class Meta:
    model = Book
    fields = ('id', 'title', 'author', 'ISBN', 'subject', 'published_date')

class BookCreateSchema(Schema):
  title: str
  author: str
  ISBN: str
  subject: str
  published_date: date 