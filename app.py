import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'CS_Department_1_is_better'

# SQLite database path
DB_PATH = 'db.sqlite3'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.cli.command('init-db')
def init_db_command():
    init_db()
    print('Database initialized.')
@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with app.open_resource('example_reports.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get_reports(sort_by, search_query, event_type):
    """
    Retrieves reports from the database with optional sorting, searching, and filtering.
    """
    conn = get_db()
    cur = conn.cursor()

    # Base query with placeholders for filtering and sorting
    query = '''
    SELECT name, event, event_type, date_attended
    FROM reports
    WHERE name LIKE ?
    '''
    query_params = [f'%{search_query}%']  # Using LIKE for partial match search

    # Add filtering by event_type if provided
    if event_type:
        query += ' AND event_type = ?'
        query_params.append(event_type)

    # Add sorting logic based on the sort_by parameter
    if sort_by == 'event':
        query += ' ORDER BY event'
    elif sort_by == 'event_desc':
        query += ' ORDER BY event DESC'
    elif sort_by == 'name_desc':
        query += ' ORDER BY name DESC'
    elif sort_by == "date_attended":
        query += ' ORDER BY date_attended'
    elif sort_by == "date_attended_desc":
        query += ' ORDER BY date_attended DESC'
    else:  # Default sorting by name
        query += ' ORDER BY name'

    # Execute the query with the accumulated parameters
    cur.execute(query, query_params)
    return cur.fetchall()

@app.route('/index')
def index():
    user = session.get('user')
    if user:
        db = get_db()
        cursor = db.execute('''
            SELECT events.event_name FROM events
            JOIN user_events ON events.id = user_events.event_id
            WHERE user_events.user_id = ? 
        ''', (user['id'],))
        attended_events = cursor.fetchall()
        return render_template('index.html', user=user, attended_events=attended_events)
    else:
        return redirect(url_for('login'))

@app.route('/reports')
def reports():
    search_query = request.args.get('search', '').strip()
    event_type = request.args.get('event_type', '')
    sort_by = request.args.get('sort', 'name')
    reports = get_reports(sort_by, search_query, event_type)

    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT event_type FROM reports')
    event_types = cur.fetchall()

    return render_template('reports.html', reports=reports, event_types=event_types)

@app.route('/events', methods=['GET', 'POST'])
def events():
    db = get_db()
    user = session.get('user')
    user_id = user['id']
    user_role = user.get('role')
    selected_date = request.args.get('selected_date')

    if request.method == 'POST':
        if user_role == 'faculty' and 'event_name' in request.form:
            #Add new event
            event_name = request.form['event_name']
            description = request.form['event_description']
            date = request.form['event_date']
            start = request.form['start_time']
            end = request.form['end_time']
            db.execute('INSERT INTO events (event_name, event_description, event_date, start_time, end_time) VALUES (?, ?, ?,?,?)', (event_name, description, date, start, end))
            db.commit()
            
        elif user_role == 'faculty' and 'remove_event_id' in request.form:
            # Remove an existing event
            event_id = request.form['remove_event_id']
            db.execute('DELETE FROM events WHERE id = ?', (event_id,))
            db.commit()
            
        elif user_role == 'student' and 'attend_event_id' in request.form:
            # Mark event as attended
            event_id = request.form['attend_event_id']
            db.execute('INSERT OR IGNORE INTO user_events (user_id, event_id) VALUES (?, ?)', (user_id, event_id))
            db.commit()

        return redirect(url_for('events'))

    if selected_date:
        events = db.execute('SELECT id, event_name, event_description FROM events WHERE event_date = ?', (selected_date,)).fetchall()
        attended_events = db.execute('SELECT event_id FROM user_events WHERE user_id = ?', (user_id,)).fetchall()
        attended_event_ids = {row['event_id'] for row in attended_events}
        events_data = [
            {
                'id': event['id'],
                'event_name': event['event_name'],
                'event_description': event['event_description'],
                'attended': event['id'] in attended_event_ids
            }
            for event in events
        ]
        return jsonify(events=events_data)

    events_list = db.execute('SELECT id, event_name FROM events').fetchall()
    attended_cursor = db.execute('SELECT event_id FROM user_events WHERE user_id = ?', (user_id,))
    attended_event_ids = {row['event_id'] for row in attended_cursor.fetchall()}

    if user_role == 'student':
        return render_template('events_student.html', events=events_list, attended_event_ids=attended_event_ids)
    else:
        return render_template('events.html', events=events_list, attended_event_ids=attended_event_ids)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form.get('role')
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered. Please log in.')
            return redirect(url_for('login'))
        
        if password != confirm_password:
            flash('Passwords fields do not match')
            return redirect(url_for('register'))
        
        if not role:
            flash('Please select a role.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password, role, first_name, last_name) VALUES (?, ?, ?, ?, ?)', (email, hashed_password, role, first_name, last_name))
        db.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('registration.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            # Fetch the first and last name to display on home page
            user_id = user[0]
            first_name = user[4]
            last_name = user[5]
            role = user[3]

            session['user'] = {'id': user_id, 'first_name': first_name, 'last_name': last_name, 'role': role}
            # User is authenticated, redirect to the index page
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')


@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_descript(event_id):

    # Query the database for the event with the given ID
    db = get_db()
    if request.method == 'POST':
        new_description = request.form['edit_event_description']
        db.execute("UPDATE events SET event_description = ? WHERE id = ?", (new_description, event_id))
        db.commit()

    cur = db.execute('SELECT id, event_name, event_description, start_time, end_time FROM events WHERE id = ?', (event_id,))
    event = cur.fetchone()
    
    # Render the eventbase.html template with the specific event's data
    return render_template('description.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)

