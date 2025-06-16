from flask import Flask, render_template, request

app = Flask(__name__)

# Sample book data
book_list = [
    {"id": "book1", "title": "Atomic Habits", "price": 250, "image": "2.jpg"},
    {"id": "book2", "title": "The Alchemist", "price": 220, "image": "3.jpg"},
    {"id": "book3", "title": "1984 by George Orwell", "price": 300, "image": "6.jpg"},
    {"id": "book4", "title": "The Subtle Art of Not Giving a F*ck", "price": 270, "image": "7.jpg"},
]

@app.route("/")
def index():
    return render_template("index.html", books=book_list)

@app.route("/order/<book_id>")
def order(book_id):
    book = next((b for b in book_list if b["id"] == book_id), None)
    return render_template("order.html", book=book)

@app.route("/confirm", methods=["POST"])
def confirm():
    name = request.form.get("name")
    book_title = request.form.get("book_title")
    return render_template("thankyou.html", name=name, book=book_title)

if __name__ == "__main__":
    app.run(debug=True)
