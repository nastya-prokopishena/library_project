from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id):
        pass

    @abstractmethod
    def find_by_email(self, email):
        pass

    @abstractmethod
    def save(self, user):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass

    @abstractmethod
    def find_all(self):
        pass


class BookRepository(ABC):
    @abstractmethod
    def find_by_id(self, book_id):
        pass

    @abstractmethod
    def find_by_title(self, title):
        pass

    @abstractmethod
    def save(self, book):
        pass

    @abstractmethod
    def delete(self, book_id):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_available(self):
        pass