from flask import Flask, jsonify, render_template, session, redirect, url_for
from pymongo import MongoClient
from config import Config
from adapters.db.mongodb_repository import MongoDBUserRepository, MongoDBBookRepository
from domain.services.library_service import LibraryService
from application.commands import UserCommands, BookCommands
from adapters.api.routes import init_routes

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB_NAME]

user_repository = MongoDBUserRepository(db)
book_repository = MongoDBBookRepository(db)

library_service = LibraryService(user_repository, book_repository)

user_commands = UserCommands(library_service)
book_commands = BookCommands(library_service)

api_routes = init_routes(user_commands, book_commands)
app.register_blueprint(api_routes, url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books')
def books():
    return render_template('books.html')


@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')


@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
