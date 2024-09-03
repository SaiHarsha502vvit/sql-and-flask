from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from os import getenv
from dotenv import load_dotenv
import datetime
from utils.home import *
from utils.loginregister import *
from utils.book import *
from utils.search import *
from utils.user import *
from utils.orders import *

load_dotenv()
mysql_host = getenv('MYSQL_HOST', None)
mysql_user = getenv('MYSQL_USER', None)
mysql_password = getenv('MYSQL_PASSWORD', None)
mysql_db = getenv('MYSQL_DB', None)

app = Flask(__name__)

app.config['MYSQL_HOST'] = mysql_host
app.config['MYSQL_USER'] = mysql_user
app.config['MYSQL_PASSWORD'] = mysql_password
app.config['MYSQL_DB'] = mysql_db
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # secret key for session encryption

mysql = MySQL(app)


def get_form_data(fields):
    return {field: str(request.form.get(field)) for field in fields}


@app.route("/")
def home_route():
    books_data = all_books(mysql)
    genre_data = all_genre(mysql)
    return render_template("home.html", books_data=books_data, genre_data=genre_data)


@app.route("/customerindex", methods=["POST", "GET"])
def customer_index_route():
    books_data = all_books(mysql)
    genre_data = all_genre(mysql)
    return render_template("customerindex.html", books_data=books_data, genre_data=genre_data)


@app.route("/adminindex", methods=["POST", "GET"])
def admin_index_route():
    books_data = all_books(mysql)
    genre_data = all_genre(mysql)
    return render_template("adminindex.html", books_data=books_data, genre_data=genre_data)


@app.route("/register", methods=["POST", "GET"])
def register_route():
    if request.method == "POST":
        username = str(request.form.get("username"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        email = str(request.form.get("email"))
        password = str(request.form.get("password"))
        phone = str(request.form.get("phone"))
        country = str(request.form.get("country"))
        state = str(request.form.get("state"))
        pincode = str(request.form.get("pincode"))
        address = str(request.form.get("address"))

        response = register(mysql, username, fname, lname, email, password, phone, country, state, pincode, address)

        if response == 1:
            return render_template("login.html", response=response)
        else:
            return render_template("register.html", response=response)

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login_route():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        account = request.form.get("account")

        if account == "customer":
            response = customer_login(mysql, username, password, account)
            if response == 1:
                session["userID"] = username
                session["accountType"] = account
                return redirect(url_for("customer_index_route"))
            else:
                return render_template("login.html", response=response)

        if account == "admin":
            response = admin_login(mysql, username, password, account)
            if response == 1:
                session["userID"] = username
                session["accountType"] = account
                return redirect(url_for("admin_index_route"))
            else:
                return render_template("login.html", response=response)

    return render_template("login.html")


@app.route("/search", methods=["POST", "GET"])
def search_route():
    if request.method == "POST":
        search = str(request.form.get("search"))
        query = str(request.form.get("query"))

        if search == "title":
            books_data = search_title(mysql, query)
            return render_template("search.html", books_data=books_data, search=search)

        if search == "genre":
            books_data = search_genre(mysql, query)
            return render_template("search.html", books_data=books_data, search=search)

        if search == "author":
            books_data = search_author(mysql, query)
            return render_template("search.html", books_data=books_data, search=search)

    return render_template("search.html")


@app.route("/customersearch", methods=["POST", "GET"])
def customer_search_route():
    if request.method == "POST":
        search = str(request.form.get("search"))
        query = str(request.form.get("query"))

        if search == "title":
            books_data = search_title(mysql, query)
            return render_template("customersearch.html", books_data=books_data, search=search)

        if search == "genre":
            books_data = search_genre(mysql, query)
            return render_template("customersearch.html", books_data=books_data, search=search)

        if search == "author":
            books_data = search_author(mysql, query)
            return render_template("customersearch.html", books_data=books_data, search=search)

    return render_template("customersearch.html")


@app.route("/books", methods=["POST", "GET"])
def books_route():
    books_data = all_books(mysql)
    genre_data = all_genre(mysql)
    return render_template("books.html", books_data=books_data, genre_data=genre_data)


@app.route("/addBook", methods=["POST", "GET"])
def add_book_route():
    if request.method == "POST":
        fields = ["bookID", "title", "genre", "fname", "lname", "year", "price", "country", "stock"]
        form_data = get_form_data(fields)

        response = add_book(mysql, **form_data)
        books_data = all_books(mysql)
        genre_data = all_genre(mysql)
        return render_template("books.html", books_data=books_data, genre_data=genre_data, response=response)

    return redirect(url_for("books_route"))


@app.route("/updateBook", methods=["POST", "GET"])
def update_book_route():
    if request.method == "POST":
        fields = ["bookID", "price1", "price2", "fname", "lname", "country"]
        form_data = get_form_data(fields)

        response = update_book(mysql, **form_data)
        books_data = all_books(mysql)
        genre_data = all_genre(mysql)
        return render_template("books.html", books_data=books_data, genre_data=genre_data, response=response)

    return redirect(url_for("books_route"))


@app.route("/deleteBook", methods=["POST", "GET"])
def delete_book_route():
    if request.method == "POST":
        fields = ["bookID", "fname", "lname", "country"]
        form_data = get_form_data(fields)

        response = delete_book(mysql, **form_data)
        return handle_book_response(response)

    return redirect(url_for("books_route"))


@app.route("/bookdetail<subject>", methods=["POST", "GET"])
def book_details_route(subject):
    book_data = book_detail(mysql, subject)
    return render_template("bookdetail.html", book_data=book_data)


@app.route("/bookDetailsAdmin<subject>", methods=["POST", "GET"])
def book_details_admin_route(subject):
    book_data = book_detail(mysql, subject)
    return render_template("bookdetail2.html", book_data=book_data)


@app.route("/inventory", methods=["POST", "GET"])
def inventory_route():
    book_data = inventory(mysql)
    return render_template("inventory.html", book_data=book_data)


@app.route("/buyBook<bookID>", methods=["POST", "GET"])
def buy_book_route(bookID):
    if request.method == "POST":
        quantity = str(request.form.get("quantity"))
        book_data = total_book_price(mysql, bookID, quantity)
        total_price = int(book_data[1]) * int(quantity)
        return render_template("payment.html", book_data=book_data, quantity=quantity, total_price=total_price)

    return "USE POST METHOD ONLY"


@app.route("/pay<isbn>/<quantity>/<total>", methods=["POST", "GET"])
def pay_route(isbn, quantity, total):
    if request.method == "POST":
        pay = str(request.form.get("pay"))

        response = orders(mysql, isbn, quantity, total, pay, session["userID"])
        return redirect(url_for('order_confirmation_route', response=response))

    return "USE POST METHOD ONLY"


@app.route("/orderconfirmation<response>", methods=["POST", "GET"])
def order_confirmation_route(response):
    return render_template("orderconfirmation.html", response=response)


@app.route("/users", methods=["POST", "GET"])
def users_route():
    admin_data = admin(mysql)
    customer_data = customers(mysql)
    return render_template("users.html", admin_data=admin_data, customer_data=customer_data)


@app.route("/myorders", methods=["POST", "GET"])
def orders_route():
    user_id = session.get("userID")
    account_type = session.get("accountType")

    if account_type is None or user_id is None:
        return "ERROR"

    if account_type == "admin":
        data = all_orders(mysql, user_id)
        return render_template("myorders.html", data=data, account_type=account_type)

    if account_type == "customer":
        data = my_order(mysql, user_id)
        return render_template("myorders.html", data=data, account_type=account_type)

    return "ERROR"


@app.route("/myaccount", methods=["POST", "GET"])
def my_account_route():
    user_id = session.get("userID")
    account_type = session.get("accountType")

    if account_type is None or user_id is None:
        return "ERROR"

    if account_type == "admin":
        data = admin_account(mysql, user_id)
        return render_template("myaccount.html", data=data, account_type=account_type)

    if account_type == "customer":
        data = customer_account(mysql, user_id)
        return render_template("myaccount.html", data=data, account_type=account_type)

    return "ERROR"


@app.route("/contactUs", methods=["POST", "GET"])
def contact_us_route():
    if request.method == "POST":
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        email = str(request.form.get("email"))
        message = str(request.form.get("message"))
        timestamp = datetime.datetime.now()
        response = contact_us(mysql, fname, lname, email, message, timestamp)
        if response == 1:
            return "Message Submitted"
        else:
            return "Failed to add message"

    return "Use POST METHOD ONLY"


@app.route("/logout", methods=["GET", "POST"])
def logout_route():
    session.pop("userID", None)
    session.pop("accountType", None)
    books_data = all_books(mysql)
    genre_data = all_genre(mysql)
    return render_template("home.html", books_data=books_data, genre_data=genre_data)


if __name__ == "__main__":
    app.run(debug=True)
