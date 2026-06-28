from fastapi import Body, FastAPI
import uvicorn

app = FastAPI()

books = [
    {"title": "Clean Code", "author": "Robert C. Martin", "price": 45.99},
    {"title": "Effective Java", "author": "Joshua Bloch", "price": 52.50},
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "price": 67.99,
    },
    {"title": "Spring in Action", "author": "Craig Walls", "price": 49.99},
    {"title": "Python Crash Course", "author": "Eric Matthes", "price": 39.95},
    {"title": "Fluent Python", "author": "Luciano Ramalho", "price": 59.99},
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "price": 44.50},
    {"title": "Refactoring", "author": "Martin Fowler", "price": 54.99},
    {"title": "Head First Design Patterns", "author": "Eric Freeman", "price": 47.75},
    {"title": "Java Concurrency in Practice", "author": "Brian Goetz", "price": 58.00},
]


@app.get("/books")
def findAll():
    return books


@app.get("/book/{number}")
def findByNumber(number: int):
    return books[number]


@app.get("/book/")
def retrieveTitle(number: int):
    return books[number]["title"]


@app.post("/book")
def addBook(book=Body()):
    books.append(book)


@app.delete("/book/{number}")
def deleteByNumber(number: int):
    books.pop(number - 1)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
