from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from app.libs.redprint import Redprint
from app.models.book import Book
from app.validators.forms import BookSearchForm

api = Redprint('book')
#‘book’是self.name中的name

@api.route('/search')
def search():
    form = BookSearchForm().validate_for_api()
    #%,sql模糊查询的条件
    q = '%' + form.q.data + '%'
    #like模糊查询
    books = Book.query.filter(
        or_(Book.title.like(q), Book.publisher.like(q))).all()
    books = [book.hide('summary') for book in books]
    return jsonify(books)

@api.route('/<isbn>/detail')
def detail(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(book)



# #url只是定位资源，应该使用HTTP动词操作资源
# @api.route('', methods=['GET'])#查询资源
# def get_book():
#     return 'get book'
#
# @api.route('', methods=['POST'])#新增资源
# def create_book():
#     return 'create book'