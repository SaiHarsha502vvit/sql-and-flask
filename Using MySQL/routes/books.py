from flask import Blueprint, request, render_template, redirect, url_for
from utils.book import addBook, updateBook, deleteBook, allBooks, allGenre, bookDetail

books_bp = Blueprint('books', __name__)

def get_form_data(fields):
    return {field: str(request.form.get(field)) for field in fields}

def handle_book_response(mysql, response):
    booksData = allBooks(mysql)
    genreData = allGenre(mysql)
    return render_template("books.html", booksData=booksData, genreData=genreData, response=response)

@books_bp.route("/addBook", methods=["POST", "GET"])
def addBookRoute():
    if request.method == "POST":
        fields = ["bookID", "title", "genre", "fname", "lname", "year", "price", "country", "stock"]
        form_data = get_form_data(fields)

        response = addBook(mysql, **form_data)
        return handle_book_response(mysql, response)

    return redirect(url_for("books.booksRoute"))

@books_bp.route("/updateBook", methods=["POST", "GET"])
def updateBookRoute():
    if request.method == "POST":
        fields = ["bookID", "price1", "price2", "fname", "lname", "country"]
        form_data = get_form_data(fields)

        response = updateBook(mysql, **form_data)
        return handle_book_response(mysql, response)

    return redirect(url_for("books.booksRoute"))

@books_bp.route("/deleteBook", methods=["POST", "GET"])
def deleteBookRoute():
    if request.method == "POST":
        fields = ["bookID", "fname", "lname", "country"]
        form_data = get_form_data(fields)

        response = deleteBook(mysql, **form_data)
        return handle_book_response(mysql, response)

    return redirect(url_for("books.booksRoute"))

@books_bp.route("/bookdetail<subject>", methods=["POST", "GET"])
def bookDetailsRoute(subject):
    bookData = bookDetail(mysql, subject)
    return render_template("bookdetail.html", bookData=bookData)

@books_bp.route("/bookDetailsAdmin<subject>", methods=["POST", "GET"])
def bookDetailsAdminRoute(subject):
    bookData = bookDetail(mysql, subject)
    return render_template("bookdetail2.html", bookData=bookData)