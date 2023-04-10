import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_patient(conn, form_data):
    cur = conn.cursor()

    cur.execute("INSERT INTO waitlist (name, description, severity) VALUES (?, ?, ?)",
                (form_data.get('name'), form_data.get('description'), int(form_data.get('severity'))))
    
    conn.commit()


@app.route("/")
def patient_view():
    return render_template('patient_view.html')

@app.route("/waitlist/add", methods=['GET', 'POST'])
def new_patient_form():
    if request.method == 'POST':
        conn = get_db_connection()
        add_patient(conn, request.form)
        conn.close()
        return redirect(url_for('patient_view'))
    
    return render_template('new_patient_form.html')

if __name__ == "__main__":
    app.run(debug=True, port=4356)