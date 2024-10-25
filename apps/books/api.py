from ninja import NinjaAPI
from apps.books.models import Book
from apps.books.schemas import BookSchema, BookCreateSchema

app = NinjaAPI()

@app.get('books/', response=list[BookSchema])
def get_books(request):
  return Book.objects.all()

@app.post('books/', response=BookSchema)
def create_book(request, book: BookCreateSchema):
  book_data = book.model_dump()
  book_model = Book.objects.create(**book_data)
  return book_model