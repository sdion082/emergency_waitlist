import sqlite3

from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
waitlist_order_cache = None

### FUNCTIONS ###

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_waitlist(conn):
    global waitlist_order_cache
    waitlist = conn.execute('''SELECT *, (severity*10 + (strftime("%M","now") - strftime("%M",arrival)) * 0.1) AS priority_by_severity_and_arrival_time
    FROM waitlist
    ORDER BY priority_by_severity_and_arrival_time DESC''').fetchall()
    waitlist_order = {}
    for position, patient in enumerate(waitlist):
        waitlist_order[patient['id']] = (position, patient['name'])
    waitlist_order_cache = waitlist_order
    return waitlist
    
def get_patient(conn, patient_id):
    return conn.execute('SELECT * FROM waitlist WHERE id=?', (patient_id,)).fetchone()

def set_patient_progress(conn, patient_id, progress):
    cur = conn.cursor()
    cur.execute("UPDATE waitlist SET in_progress=? WHERE id=?", (progress, patient_id))
    success = cur.rowcount
    conn.commit()
    patient_data = {'in_progress': get_patient(conn, patient_id)['in_progress']} if success > 0 else False
    return patient_data

def add_patient(conn, form_data):
    cur = conn.cursor()
    cur.execute("INSERT INTO waitlist (name, description, severity) VALUES (?, ?, ?)",
                (form_data.get('name'), form_data.get('description'), int(form_data.get('severity'))))
    insert_id = cur.lastrowid
    conn.commit()
    get_waitlist(conn) # Update waitlist order cache
    return insert_id

def remove_patient(conn, patient_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM waitlist WHERE id=?", (patient_id,))
    conn.commit()
    get_waitlist(conn) # Update waitlist order cache

### ROUTES ###

@app.route("/", methods=['GET', 'POST'])
def new_patient_form():
    if request.method == 'POST':
        conn = get_db_connection()
        patient_id = add_patient(conn, request.form)
        conn.close()
        return redirect(url_for('patient_view', patient_id=patient_id))
    
    return render_template('new_patient_form.html')

## PATIENT ##

@app.route("/patient/<patient_id>")
def patient_view(patient_id):
    return render_template('patient_view.html', patient_id=patient_id)

@app.route("/patient/<patient_id>/wait_time")
def get_wait_time(patient_id):
    if waitlist_order_cache is None:
        conn = get_db_connection()
        get_waitlist(conn)
        conn.close()
    position = waitlist_order_cache.get(int(patient_id), (-1, None))
    return {'position': position[0], 'name': position[1]}

@app.route("/goodbye")
def goodbye_view():
    return render_template('goodbye.html')

## ADMIN ##

@app.route("/admin")
def waitlist_view():
    conn = get_db_connection()
    waitlist = get_waitlist(conn)
    conn.close()
    return render_template('waitlist.html', waitlist=waitlist)

@app.route("/admin/<patient_id>/view")
def doctor_view(patient_id):
    conn = get_db_connection()
    patient = get_patient(conn, patient_id)
    conn.close()
    
    if patient is None:
        abort(404)
    return render_template('doctor_view.html', patient=patient)

@app.route("/admin/<patient_id>/set_progress/<progress>", methods=['POST'])
def change_patient_progress(patient_id, progress):
    conn = get_db_connection()
    success = set_patient_progress(conn, patient_id, progress)
    conn.close()
    return {'success': success}

@app.route("/admin/<patient_id>/finished")
def patient_finished(patient_id):
    conn = get_db_connection()
    patient_id = remove_patient(conn, patient_id)
    conn.close()
    return redirect(url_for('waitlist_view'))

### MAIN LOGIC ###

if __name__ == "__main__":
    app.run(debug=True, port=4356)