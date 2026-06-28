from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    rating: float

    def __init__(self, id, title, author, rating):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str
    rating: float


BOOKS = [
    Book(1, "Clean Code", "Robert C. Martin", 4.8),
    Book(2, "Effective Java", "Joshua Bloch", 4.9),
    Book(3, "Designing Data-Intensive Applications", "Martin Kleppmann", 4.9),
    Book(4, "The Pragmatic Programmer", "Andrew Hunt", 4.7),
    Book(5, "Python Crash Course", "Eric Matthes", 4.6),
]


@app.get("/books")
def retrieveBooks():
    return BOOKS


@app.get("/books/{bookId}")
def getBooksById(bookId: int = Path(gt=1)):
    return next((book for book in BOOKS if book.id == bookId), None)


@app.get("/bookRating")
def getBooksByRating(rating: float = Query(gt=1)):
    for book in BOOKS:
        if book.rating == rating:
            return book
    # return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.post("/book")
def addBook(book: BookRequest):
    newBook = Book(**book.model_dump())
    BOOKS.append(addId(newBook))


def addId(newBook: Book):
    newBook.id = BOOKS[-1].id + 1 if (len(BOOKS) > 0) else 1
    # if BOOKS.length > 0:
    #     newBook.id = BOOKS[-1].id + 1
    # else:
    #     newBook.id = 1
    return newBook
