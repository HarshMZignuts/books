from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date:int

    def __init__(self,id, title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1,max_length=100)
    rating: int = Field(gt=0,lt=6)
    published_date: int = Field(gt=1999,lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "tile": "A new book",
                "author": "Author name",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2012
            }
        }
    }
        

BOOKS = [
    Book(id=1,title='Computer science pro',author='HKM',description= 'Very nice book!',rating=5,published_date=2026),
    Book(id=2,title='Be fast with fast api',author='HKM',description= 'Very good book!',rating=5,published_date=2026),
    Book(id=3,title='Master of endpoint',author='HKM',description= 'Very awsome book!',rating=5,published_date=2025),
    Book(id=4,title='HKM1',author='Author1',description= 'Book description',rating=2,published_date=2000),
    Book(id=5,title='HKM2',author='Author1',description= 'Book description',rating=3,published_date=2024),
    Book(id=6,title='HKM3',author='Author1',description= 'Book description',rating=1,published_date=2000)
]

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id:int = Path(gt= 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')
        
@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return

@app.get("/book/publish/",status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(publish_date:int = Query(gt=1999,lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == publish_date:
            books_to_return.append(book)

    return books_to_return

@app.post("/books/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    # new_book = Book(**book_request.dict()) // in pydantic2 .dict() is debricared
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))



def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    
    return book

@app.put("/books/update-book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item not found")
        
@app.delete("/book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt= 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item not found")