from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, static_url_path='/static')

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="quote_of_the_day"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quotes ORDER BY RAND() LIMIT 1")
    random_quotes = cursor.fetchall()
    cursor.close()

    return render_template('index.html', random_quotes=random_quotes)

@app.route('/search')
def search():
    author = request.args.get('author')
    if author:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM quotes WHERE author LIKE %s", (f"%{author}%",))
        results = cursor.fetchall()
        cursor.close()
        return render_template('search_results.html', results=results)
    return render_template('search_results.html', results="No Quotes found")

@app.route('/author/<author>')
def author_quotes(author):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quotes WHERE author = %s", (author,))
    results = cursor.fetchall()
    cursor.close()
    return render_template('author_quotes.html', author=author, results=results)

if __name__ == '__main__':
    app.run(debug=True)
