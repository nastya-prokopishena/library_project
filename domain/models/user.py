class User:
    def __init__(self, name, email, password, user_id=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.borrowed_books = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book_id):
        for i, book in enumerate(self.borrowed_books):
            if book.book_id == book_id:
                return self.borrowed_books.pop(i)
        return None

    def has_book(self, book_id):
        return any(book.book_id == book_id for book in self.borrowed_books)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "borrowed_books": [book.to_dict() for book in self.borrowed_books]
        }

    @classmethod
    def from_dict(cls, data):
        from domain.models.book import Book
        user = cls(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password")
        )
        user.borrowed_books = [Book.from_dict(book_data) for book_data in data.get("borrowed_books", [])]
        return user