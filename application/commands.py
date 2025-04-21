class UserCommands:
    def __init__(self, library_service):
        self.library_service = library_service

    def register_user(self, name, email, password):
        from domain.models.user import User
        user = User(name=name, email=email, password=password)
        return self.library_service.register_user(user)

    def login(self, email, password):
        return self.library_service.authenticate_user(email, password)

    def borrow_book(self, user_id, book_id):
        return self.library_service.borrow_book(user_id, book_id)

    def return_book(self, user_id, book_id):
        return self.library_service.return_book(user_id, book_id)

    def get_user_books(self, user_id):
        return self.library_service.get_user_books(user_id)


class BookCommands:
    def __init__(self, library_service):
        self.library_service = library_service

    def add_book(self, title, author, genre):
        from domain.models.book import Book
        book = Book(title=title, author=author, genre=genre)
        return self.library_service.add_book(book)

    def get_all_books(self):
        return self.library_service.get_all_books()

    def get_available_books(self):
        return self.library_service.get_available_books()