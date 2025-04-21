from abc import ABC, abstractmethod


class UserPort(ABC):
    @abstractmethod
    def register(self, name, email, password):
        pass

    @abstractmethod
    def login(self, email, password):
        pass

    @abstractmethod
    def get_user_info(self, user_id):
        pass

    @abstractmethod
    def update_user(self, user_id, data):
        pass

    @abstractmethod
    def borrow_book(self, user_id, book_id):
        pass

    @abstractmethod
    def return_book(self, user_id, book_id):
        pass

    @abstractmethod
    def get_borrowed_books(self, user_id):
        pass