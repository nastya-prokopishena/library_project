class LibraryService:
    def __init__(self, user_repository, book_repository):
        self.user_repository = user_repository
        self.book_repository = book_repository

    def register_user(self, user):
        existing_user = self.user_repository.find_by_email(user.email)
        if existing_user:
            raise ValueError(f"User with email {user.email} already exists")

        return self.user_repository.save(user)

    def authenticate_user(self, email, password):
        user = self.user_repository.find_by_email(email)
        if not user or user.password != password:
            return None
        return user

    def add_book(self, book):
        return self.book_repository.save(book)

    def borrow_book(self, user_id, book_id):
        user = self.user_repository.find_by_id(user_id)
        book = self.book_repository.find_by_id(book_id)

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        if not book:
            raise ValueError(f"Book with id {book_id} not found")

        if not book.available:
            raise ValueError(f"Book '{book.title}' is not available")

        book.mark_as_borrowed()
        user.borrow_book(book)

        self.book_repository.save(book)
        self.user_repository.save(user)

        return book

    def return_book(self, user_id, book_id):
        user = self.user_repository.find_by_id(user_id)
        book = self.book_repository.find_by_id(book_id)

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        if not book:
            raise ValueError(f"Book with id {book_id} not found")

        if not user.has_book(book_id):
            raise ValueError(f"User does not have this book")

        returned_book = user.return_book(book_id)
        returned_book.mark_as_available()

        self.book_repository.save(returned_book)
        self.user_repository.save(user)

        return returned_book

    def get_all_books(self):
        return self.book_repository.find_all()

    def get_available_books(self):
        return self.book_repository.find_available()

    def get_user_books(self, user_id):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user.borrowed_books