# Task Tracker API

## About

Task Tracker API is a small Flask application for creating, viewing, updating, filtering, and deleting tasks. It uses SQLite for data storage and includes a simple browser interface.

## Features

- Create tasks with a title, due date, description, and status.
- View all tasks or filter them by status.
- Update task status and other task fields through the API.
- Delete tasks.
- Reject empty titles, invalid dates, past due dates, and unsupported statuses.

## Project Files

- `app.py` contains the Flask routes and validation.
- `database.py` contains the SQLite database functions.
- `page/index.html` contains the page structure.
- `page/css/script.css` contains the page styles.
- `page/js/script.js` contains the browser behavior.
- `tasks.db` stores the task data locally.

## Setup

1. Install Python 3.10 or newer.
2. Install the dependencies:

	```bash
	pip install -r requirements.txt
	```

3. Start the application:

	```bash
	python app.py
	```

4. Open `http://127.0.0.1:5000` in a browser.

## API Routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/tasks` | Return all tasks |
| GET | `/api/tasks/<task_id>` | Return one task |
| POST | `/api/tasks` | Create a task |
| PUT | `/api/tasks/<task_id>` | Update a task |
| DELETE | `/api/tasks/<task_id>` | Delete a task |

## AI Use Acknowledgement

GitHub Copilot was used as an AI coding assistant during this project. AI assistance was used to add simple comments, identify bugs, repair Python and JavaScript issues, connect the Flask application to the page files, improve CSS consistency, and help test the API workflows.

The project was reviewed and tested in Visual Studio Code. The tools used included the VS Code editor, GitHub Copilot, Python, Flask, Flask-CORS, SQLite, JavaScript syntax checking with Node.js, and Flask's test client. The developer remained responsible for reviewing the suggestions, choosing the changes, and checking that the application worked correctly.
