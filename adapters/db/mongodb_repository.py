from ports.repository import UserRepository, BookRepository
from domain.models.user import User
from domain.models.book import Book
from pymongo import MongoClient


class MongoDBUserRepository(UserRepository):
    def __init__(self, db):
        self.collection = db.users

    def find_by_id(self, user_id):
        user_data = self.collection.find_one({"_id": user_id})
        if user_data:
            user_data["user_id"] = user_data.pop("_id")
            return User.from_dict(user_data)
        return None

    def find_by_email(self, email):
        user_data = self.collection.find_one({"email": email})
        if user_data:
            user_data["user_id"] = user_data.pop("_id")
            return User.from_dict(user_data)
        return None

    def save(self, user):
        user_dict = user.to_dict()

        if user.user_id is None:
            # Генеруємо новий ID, якщо це новий користувач
            last_user = self.collection.find_one(sort=[("_id", -1)])
            if last_user:
                new_id = int(last_user["_id"]) + 1
            else:
                new_id = 1
            user.user_id = str(new_id)
            user_dict["_id"] = user.user_id
        else:
            user_dict["_id"] = user_dict.pop("user_id")

        self.collection.replace_one({"_id": user_dict["_id"]}, user_dict, upsert=True)
        return user

    def delete(self, user_id):
        result = self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0

    def find_all(self):
        users = []
        for user_data in self.collection.find():
            user_data["user_id"] = user_data.pop("_id")
            users.append(User.from_dict(user_data))
        return users


class MongoDBBookRepository(BookRepository):
    def __init__(self, db):
        self.collection = db.books

    def find_by_id(self, book_id):
        book_data = self.collection.find_one({"_id": book_id})
        if book_data:
            book_data["book_id"] = book_data.pop("_id")
            return Book.from_dict(book_data)
        return None

    def find_by_title(self, title):
        book_data = self.collection.find_one({"title": title})
        if book_data:
            book_data["book_id"] = book_data.pop("_id")
            return Book.from_dict(book_data)
        return None

    def save(self, book):
        book_dict = book.to_dict()

        if book.book_id is None:
            # Генеруємо новий ID, якщо це нова книга
            last_book = self.collection.find_one(sort=[("_id", -1)])
            if last_book:
                new_id = int(last_book["_id"]) + 1
            else:
                new_id = 1
            book.book_id = str(new_id)
            book_dict["_id"] = book.book_id
        else:
            book_dict["_id"] = book_dict.pop("book_id")

        self.collection.replace_one({"_id": book_dict["_id"]}, book_dict, upsert=True)
        return book

    def delete(self, book_id):
        result = self.collection.delete_one({"_id": book_id})
        return result.deleted_count > 0

    def find_all(self):
        books = []
        for book_data in self.collection.find():
            book_data["book_id"] = book_data.pop("_id")
            books.append(Book.from_dict(book_data))
        return books

    def find_available(self):
        books = []
        for book_data in self.collection.find({"available": True}):
            book_data["book_id"] = book_data.pop("_id")
            books.append(Book.from_dict(book_data))
        return books