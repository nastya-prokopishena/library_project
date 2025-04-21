from flask import Blueprint, jsonify, request, session
from application.commands import UserCommands, BookCommands

api = Blueprint('api', __name__)


def init_routes(user_commands, book_commands):
    @api.route('/register', methods=['POST'])
    def register():
        data = request.json
        try:
            user = user_commands.register_user(
                name=data.get('name'),
                email=data.get('email'),
                password=data.get('password')
            )
            return jsonify({
                'success': True,
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email
            }), 201
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    @api.route('/login', methods=['POST'])
    def login():
        data = request.json
        user = user_commands.login(
            email=data.get('email'),
            password=data.get('password')
        )

        if user:
            session['user_id'] = user.user_id
            return jsonify({
                'success': True,
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    @api.route('/logout', methods=['POST'])
    def logout():
        session.pop('user_id', None)
        return jsonify({'success': True}), 200

    @api.route('/books', methods=['GET'])
    def get_books():
        available_only = request.args.get('available', 'false').lower() == 'true'

        if available_only:
            books = book_commands.get_available_books()
        else:
            books = book_commands.get_all_books()

        return jsonify({
            'success': True,
            'books': [book.to_dict() for book in books]
        }), 200

    @api.route('/books', methods=['POST'])
    def add_book():
        data = request.json
        book = book_commands.add_book(
            title=data.get('title'),
            author=data.get('author'),
            genre=data.get('genre')
        )

        return jsonify({
            'success': True,
            'book': book.to_dict()
        }), 201

    @api.route('/users/<user_id>/books', methods=['GET'])
    def get_user_books(user_id):
        try:
            books = user_commands.get_user_books(user_id)
            return jsonify({
                'success': True,
                'books': [book.to_dict() for book in books]
            }), 200
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 404

    @api.route('/users/<user_id>/books/<book_id>/borrow', methods=['POST'])
    def borrow_book(user_id, book_id):
        try:
            book = user_commands.borrow_book(user_id, book_id)
            return jsonify({
                'success': True,
                'book': book.to_dict()
            }), 200
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    @api.route('/users/<user_id>/books/<book_id>/return', methods=['POST'])
    def return_book(user_id, book_id):
        try:
            book = user_commands.return_book(user_id, book_id)
            return jsonify({
                'success': True,
                'book': book.to_dict()
            }), 200
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    return api