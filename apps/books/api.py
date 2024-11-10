from ninja import NinjaAPI
from apps.books.models import Book
from apps.books.schemas import BookSchema, BookCreateSchema
import requests
import json
import re
import os
from config.env import BASE_DIR, env

# Lade die Umgebungsvariablen aus der .env-Datei
env.read_env(os.path.join(BASE_DIR, '.env'))

app = NinjaAPI()

@app.get('books/', response=list[BookSchema])
def get_books(request):
    return Book.objects.all()

@app.post('books/', response=BookSchema)
def create_book(request, book: BookCreateSchema):
    book_data = book.model_dump()
    book_model = Book.objects.create(**book_data)
    return book_model

@app.post('fetch_book_isbn/', response=BookSchema)
def fetch_book_info(request, isbn: str):
    print(isbn)
    
    # Ihr API-Schlüssel von Writesonic aus der Umgebungsvariable
    api_key = env('WRITESONIC_API_KEY')

    # API-Endpunkt
    url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"

    # Anfragepayload
    payload = {
        "input_text": f"Gib mir title, author, ISBN, subject, published_year(nur das Jahr als integer), des Buches mit der ISBN {isbn} im JSON-Format. Wenn man die ISBN auf google sucht, kommt das richtige Buch. Nur das JSON als Output!",
        "enable_google_results": True,
        "enable_memory": False
    }

    # Header mit API-Schlüssel
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": api_key
    }

    # POST-Anfrage an die API
    response = requests.post(url, json=payload, headers=headers) 

    # Überprüfung der Antwort
    if response.status_code == 200:
        data = response.json()
        print("Antwort von Writesonic:", data)
        try:
            # Extrahiere den JSON-Teil aus der Antwort
            message = data.get("message")
            json_match = re.search(r'\{.*\}', message, re.DOTALL)
            if json_match:
                book_info = json_match.group(0)
                book_info_dict = json.loads(book_info)
                # Ausgabe im Terminal
                print(json.dumps(book_info_dict, indent=4))
                
                # Buch in die Datenbank einfügen
                published_year = book_info_dict.get("published_year")
                if published_year and published_year != "Unbekannt":
                    published_year = int(published_year)
                else:
                    published_year = None

                book_data = {
                    "title": book_info_dict.get("title"),
                    "author": book_info_dict.get("author"),
                    "ISBN": book_info_dict.get("ISBN"),
                    "subject": book_info_dict.get("subject"),
                    "published_year": published_year
                }
                book_create_schema = BookCreateSchema(**book_data)
                created_book = create_book(request, book_create_schema)
                return BookSchema.from_orm(created_book)
            else:
                return {"error": "No valid JSON found in the response"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from Writesonic", "response": data}
    else:
        return {"error": response.status_code, "message": response.text}

