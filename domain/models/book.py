class Book:
    def __init__(self, title, author, genre, book_id=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = True

    def mark_as_borrowed(self):
        self.available = False

    def mark_as_available(self):
        self.available = True

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "available": self.available
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(
            book_id=data.get("book_id"),
            title=data.get("title"),
            author=data.get("author"),
            genre=data.get("genre")
        )
        book.available = data.get("available", True)
        return book