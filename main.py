from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/library"
mongo = PyMongo(app)
books = mongo.db.books

# books_ls = [
#     {"name": "Harry Potter", "author": "J. k. Rowling", "rating": 9.2},
#     {"name": "Metro 2033", "author": "Dimitry glukhovsky", "rating": 8.5}
# ]


# books.insert_many(books_ls)

# pprint.pprint(books.find_one({"rating": {"$lte": 9.0}}, {"author": 1}))
# pprint.pprint(books.count_documents({}))

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     author = db.Column(db.String(250), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#
#     def __repr__(self):
#         return f"<Book {self.title}>"
#
#
# db.create_all()
#
#
@app.route('/')
def home():
    all_books = books.find()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_name = request.form["book_name"]
        book_author = request.form["book_author"]
        book_rating = float(request.form["book_rating"])
        books.insert_one({"name": book_name, "author": book_author, "rating": book_rating})
        return redirect('/')
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        pk = request.form["pk"]
        books.update_one({"_id": ObjectId(pk)}, {"$set": {"rating": float(request.form["book_rating"])}})
        return redirect('/')
    book_id = request.args.get("pk")
    book_to_update = books.find_one({"_id": ObjectId(book_id)})
    return render_template("edit.html", book=book_to_update)


@app.route("/delete", methods=["get", "post"])
def delete():
    book_id = request.args.get("pk")
    print(type(book_id))
    books.delete_one({"_id": ObjectId(book_id)})
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
