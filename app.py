import sqlite3

from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

### FUNCTIONS ###

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_waitlist(conn):
    return conn.execute('''SELECT *, (severity*10 + (strftime("%M","now") - strftime("%M",arrival)) * 0.1) AS priority_by_severity_and_arrival_time
    FROM waitlist
    ORDER BY priority_by_severity_and_arrival_time DESC''').fetchall()
    
def get_patient(conn, patient_id):
    return conn.execute('SELECT * FROM waitlist WHERE id=?', (patient_id,)).fetchone()

def set_patient_progess(conn, patient_id, progress):
    cur = conn.cursor()
    cur.execute("UPDATE waitlist SET in_progress=? WHERE id=?", (progress, patient_id))
    conn.commit()

def add_patient(conn, form_data):
    cur = conn.cursor()
    cur.execute("INSERT INTO waitlist (name, description, severity) VALUES (?, ?, ?)",
                (form_data.get('name'), form_data.get('description'), int(form_data.get('severity'))))
    insert_id = cur.lastrowid
    conn.commit()
    return insert_id

### ROUTES ###

@app.route("/patient/<patient_id>")
def patient_view(patient_id):
    return render_template('patient_view.html')

@app.route("/", methods=['GET', 'POST'])
def new_patient_form():
    if request.method == 'POST':
        conn = get_db_connection()
        patient_id = add_patient(conn, request.form)
        conn.close()
        return redirect(url_for('patient_view', patient_id=patient_id))
    
    return render_template('new_patient_form.html')

@app.route("/admin")
def waitlist_view():
    conn = get_db_connection()
    waitlist = get_waitlist(conn)
    conn.close()
    return render_template('waitlist.html', waitlist=waitlist)

@app.route("/admin/view/<patient_id>")
def doctor_view(patient_id):
    conn = get_db_connection()
    patient = get_patient(conn, patient_id)
    #set_patient_progess(conn, patient_id, 1)
    conn.close()
    
    if patient is None:
        abort(404)
    return render_template('doctor_view.html', patient=patient)

### MAIN LOGIC ###

if __name__ == "__main__":
    app.run(debug=True, port=4356)