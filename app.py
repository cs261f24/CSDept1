import sqlite3
from flask import Flask, g, render_template

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
    Initialize the database with a table.
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

    # fetchall() gets all the rows as a list
    return cur.fetchall()

@app.route('/')
def reports():
    """
    Serves a page which shows the items sorted by name. See the file
    templates/items.html for the template. The list returned from get_items()
    is passed as the positional parameter items, which is then accessible
    within the template.
    """

    return render_template('index.html', reports=get_reports())

if __name__ == '__main__':
    app.run(debug=True)
