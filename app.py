import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for

app = Flask(__name__)

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

def get_reports():
    """
    Returns a list of reports sorted by name.
    """
    conn = get_db()
    cur = conn.cursor()

    query = '''
SELECT name, event
FROM reports
ORDER BY name'''

    cur.execute(query)
    return cur.fetchall()

@app.route('/index')
def index():
    """
    Serves the index page with welcome text.
    """
    print("Index page accessed")
    return render_template('index.html')

@app.route('/reports')
def reports():
    """
    Serves a page which shows the items sorted by name. See the file
    templates/items.html for the template. The list returned from get_items()
    is passed as the positional parameter items, which is then accessible
    within the template.
    """
    return render_template('reports.html', reports=get_reports())

# Add route to display events and add a new event
@app.route('/events', methods=['GET', 'POST'])
def events():
    db = get_db()

    if request.method == 'POST':
        # Check if the request is to add or remove an event
        if 'event_name' in request.form:
            # Add new event
            event_name = request.form['event_name']
            # Insert the new event into the database
            db.execute('INSERT INTO events (event_name) VALUES (?)', (event_name,))
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

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form data (login logic)
        username = request.form['username']
        password = request.form['password']
        # Add logic to authenticate user
        return redirect(url_for('index'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
