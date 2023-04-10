import sqlite3

from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def patient_view():
    return render_template('patient_view.html')

if __name__ == "__main__":
    app.run(debug=True, port=4356)