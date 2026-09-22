# Import date validation tools.
from datetime import date
# Import Flask tools.
from flask import Flask, jsonify, request, render_template
# Enable cross-origin requests.
from flask_cors import CORS
# Import database helpers.
import database

# Create the Flask application.
app = Flask(__name__, template_folder='page', static_folder='page', static_url_path='/page')
CORS(app)

# Allowed task statuses.
task_status = ["Not Started", "In Progress", "Completed"]

# Initialize the database when the application starts.
with app.app_context():
    database.init_db()

# Display the main page.
@app.route('/')
def index():
    return render_template('index.html')

# Return all tasks, optionally filtered by status.
@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    status_filter = request.args.get('status')
    tasks = database.get_all_tasks(status_filter)
    return jsonify({
        'success': True,
        'tasks': tasks,
        'count': len(tasks)
    }), 200

# Return one task by its ID.
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = database.get_task_by_id(task_id)
    if task:
        return jsonify({
            'success': True,
            'task': task
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Task not found'
        }), 404

# Create a new task.
@app.route('/api/tasks', methods=['POST'])
def create_task():
    # Read task data from the request body.
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            'success': False,
            'message': 'Request body must be a JSON object'
        }), 400
    title = data.get('title', '')
    due_date = data.get('due_date', '')
    description = data.get('description', '')
    status = data.get('status', 'Not Started')

    if not isinstance(title, str) or not isinstance(description, str):
        return jsonify({
            'success': False,
            'message': 'Title and description must be text'
        }), 400

    title = title.strip()
    description = description.strip()

    if due_date and not isinstance(due_date, str):
        return jsonify({
            'success': False,
            'message': 'Invalid due date format. Use YYYY-MM-DD.'
        }), 400

    # Require a task title.
    if not title:
        return jsonify({
            'success': False,
            'message': 'Title is required'
        }), 400

    # Validate the due date when one is provided.
    if due_date:
        try:
            due_date_obj = date.fromisoformat(due_date)
            if due_date_obj < date.today():
                return jsonify({
                    'success': False,
                    'message': 'Due date cannot be in the past'
                }), 400
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid due date format. Use YYYY-MM-DD.'
            }), 400

    # Validate the task status.
    if status not in task_status:
        return jsonify({
            'success': False,
            'message': f'Status must be one of {task_status}'
        }), 400

    # Save the new task in the database.
    new_task = database.create_task(
                                    title = title,
                                    due_date = due_date,
                                    description = description,
                                    status = status)
    return jsonify({
        'success': True,
        'message': 'Task created successfully',
        'task': new_task
    }), 201

# Update an existing task.
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Check that the task exists before updating it.
    existing_task = database.get_task_by_id(task_id)
    if not existing_task:
        return jsonify({
            'success': False,
            'message': 'Task not found'
        }), 404
    # Read updated fields from the request body.
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            'success': False,
            'message': 'Request body must be a JSON object'
        }), 400

    # Validate the optional title.
    title = data.get('title')
    if title is not None and (not isinstance(title, str) or not title.strip()):
        return jsonify({
            'success': False,
            'message': 'Title cannot be empty'
        }), 400

    # Validate the optional status.
    status = data.get('status')
    if status is not None and status not in task_status:
        return jsonify({
            'success': False,
            'message': f'Status must be one of {task_status}'
        }), 400

    # Validate the optional due date.
    due_date = data.get('due_date')
    if due_date:
        if not isinstance(due_date, str):
            return jsonify({
                'success': False,
                'message': 'Invalid due date format. Use YYYY-MM-DD.'
            }), 400
        try:
            due_date_obj = date.fromisoformat(due_date)
            if due_date_obj < date.today():
                return jsonify({
                    'success': False,
                    'message': 'Due date cannot be in the past'
                }), 400
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid due date format. Use YYYY-MM-DD.'
            }), 400

    # Update the task in the database.
    description = data.get('description')
    if description is not None and not isinstance(description, str):
        return jsonify({
            'success': False,
            'message': 'Description must be text'
        }), 400
    updated_task = database.update_task(
        task_id = task_id,
        title = title,  
        due_date = due_date,
        description = description,
        status = status
    )

    return jsonify({
        'success': True,    
    'message': 'Task updated successfully',
    'task': updated_task
    }), 200

# Delete an existing task.
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Check that the task exists before deleting it.
    existing_task = database.get_task_by_id(task_id)
    if not existing_task:
        return jsonify({
            'success': False,
            'message': 'Task not found'
        }), 404

    # Remove the task from the database.
    database.delete_task(task_id)
    return jsonify({
        'success': True,
        'message': 'Task deleted successfully'
    }), 200

# Start the development server when this file is run directly.
if __name__ == '__main__':
    print("Starting the Flask server...")
    app.run(debug=True, host='127.0.0.1', port=5000)    