# Import database tools.
import sqlite3
import os

# Store the database file name.
db_name = 'tasks.db'

# Create a database connection.
def get_db_connection():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

# Create the database table if needed.
def init_db():
    # Check if the database file already exists.
    if not os.path.exists(db_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create the tasks table.
        cursor.execute('''
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'Not Started'
            )
        ''')
        conn.commit()
        conn.close()

# Get all tasks.
def get_all_tasks(status=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if status and status.lower() != 'all':
        cursor.execute('SELECT * FROM tasks WHERE status = ?', (status,))
    else:
        cursor.execute('SELECT * FROM tasks')

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Get one task by ID.
def get_task_by_id(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# Add a new task.
def create_task(title, due_date, description=None, status='Not Started'):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, due_date, description, status)
        VALUES (?, ?, ?, ?)
    ''', (title.strip(), due_date, description.strip() if description else '', status))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return get_task_by_id(task_id)

# Update an existing task.
def update_task(task_id, title=None, due_date=None, description=None, status=None):
    existing_task = get_task_by_id(task_id)
    if not existing_task:
        return None

    new_title = title.strip() if title is not None else existing_task['title']
    new_due_date = due_date if due_date is not None else existing_task['due_date']
    new_description = description.strip() if description is not None else existing_task['description']
    new_status = status if status is not None else existing_task['status']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET title = ?, due_date = ?, description = ?, status = ?
        WHERE id = ?
    ''', (new_title, new_due_date, new_description, new_status, task_id))
    conn.commit()
    conn.close()
    return get_task_by_id(task_id)

# Delete a task by ID.
def delete_task(task_id):
    existing_task = get_task_by_id(task_id)
    if not existing_task:   
        return False

    conn = get_db_connection()
    cursor = conn.cursor()  
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return True