import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'CS_Department_1_is_better'

# SQLite database path
DB_PATH = 'db.sqlite3'

def get_db():
    """
    Returns a database connection.
    Creates a new connection if it doesn't exist.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

# For initializing the database through command-line
@app.cli.command('init-db')
def init_db_command():
    init_db()
    print('Database initialized.')

@app.teardown_appcontext
def close_db(exception):
    """
    Close the database connection after the request ends.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Initialize the database with tables.
    """
    db = get_db()
    
    with app.open_resource('example_reports.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get_reports(sort_by, search_query, event_type):
    conn = get_db()
    cur = conn.cursor()

    # Base query with placeholders for filtering and sorting
    query = '''
    SELECT name, event, event_type
    FROM reports
    WHERE name LIKE ?
    '''

    query_params = [f'%{search_query}%']

    # Add filtering by event_type if provided
    if event_type:
        query += ' AND event_type = ?'
        query_params.append(event_type)

    # Add sorting logic
    if sort_by == 'event':
        query += ' ORDER BY event'
    elif sort_by == 'event_desc':
        query += ' ORDER BY event DESC'
    elif sort_by == 'name_desc':
        query += ' ORDER BY name DESC'
    else:  # Default is sorting by name
        query += ' ORDER BY name'

    cur.execute(query, query_params)
    return cur.fetchall()


@app.route('/index')
def index():
    user = session.get('user')
    if user:
        return render_template('index.html', user=user)
    else:
        return render_template('login.html')

@app.route('/reports')
def reports():
    search_query = request.args.get('search', '').strip()
    event_type = request.args.get('event_type', '')
    sort_by = request.args.get('sort', 'name')  # Default sort by name
    reports = get_reports(sort_by, search_query, event_type)  # Pass all parameters

    # Fetch unique event types for the dropdown
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT event_type FROM reports')
    event_types = cur.fetchall()

    return render_template('reports.html', reports=reports, event_types=event_types)
# Add route to display events and add a new event
@app.route('/events', methods=['GET', 'POST'])
def events():
    db = get_db()

    if request.method == 'POST':
        # Check if the request is to add or remove an event
        if 'event_name' in request.form:
            # Add new event
            event_name = request.form['event_name']
            description = 'placeholder descript'
            # Insert the new event into the database
            db.execute('INSERT INTO events (event_name, event_description) VALUES (?,?)', (event_name, description))
            db.commit()
        elif 'remove_event_id' in request.form:
            #Remove an existing event
            event_id = request.form['remove_event_id']
            db.execute('DELETE FROM events WHERE id = ?', (event_id,))
            db.commit()

        # Redirect back to the events page after adding the event
        return redirect(url_for('events'))
    
    # Fetch all events to display on the page
    cur = db.execute('SELECT id, event_name, attended FROM events')
    events_list = cur.fetchall()

    return render_template('events.html', events=events_list)


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

        # Check if the email is already registered
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


        # Insert the new user into the users table
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password, role, first_name, last_name) VALUES (?, ?, ?, ?, ?)', (email, hashed_password, role, first_name, last_name))
        db.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('registration.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form data (login logic)
        email = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        # Add logic to authenticate user
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            # Fetch the first and last name to display on home page
            first_name = user[4]
            last_name = user[5]
            session['user'] = {'first_name': first_name, 'last_name': last_name}
            # User is authenticated, redirect to the index page
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')


@app.route('/description', methods=['GET', 'POST'])
def event_descript():
    db = get_db()   
    cur = db.execute('SELECT event_name, event_description FROM events')
    events = cur.fetchall()

    return render_template('eventbase.html', events=events)


if __name__ == '__main__':
    app.run(debug=True)
