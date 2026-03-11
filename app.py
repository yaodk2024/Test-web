import os
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)


def get_db():
    return psycopg2.connect(os.environ['DATABASE_URL'])


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        cur.execute("INSERT INTO messages (name, message) VALUES (%s, %s)", (name, message))
        conn.commit()
        conn.close()
        return redirect('/')

    cur.execute("SELECT name, message FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    conn.close()
    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)