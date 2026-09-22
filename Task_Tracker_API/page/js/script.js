// Find the page elements.
const taskForm = document.getElementById('taskForm');
const taskTitle = document.getElementById('taskTitle');
const taskDueDate = document.getElementById('taskDueDate');
const taskDescription = document.getElementById('taskDescription');
const taskStatus = document.getElementById('taskStatus');
const loading = document.getElementById('loading');
const emptyState = document.getElementById('emptyState');
const taskContainer = document.getElementById('taskContainer');
const toast = document.getElementById('toast');

// Start the page after it loads.
document.addEventListener('DOMContentLoaded', () => {
    taskDueDate.min = new Date().toISOString().split('T')[0];
    taskForm.addEventListener('submit', handleCreateTask);
    fetchTasks();
});

async function fetchTasks() {
    // Load all tasks from the API.
    loading.classList.remove('hidden');
    emptyState.classList.add('hidden');
    taskContainer.innerHTML = '';

    try {
        const response = await fetch('/api/tasks');
        const data = await response.json();
        if (!response.ok || !data.success) {
            throw new Error(data.message || 'Failed to fetch tasks.');
        }
        renderTasks(data.tasks);
    } catch (error) {
        console.error('Error fetching tasks:', error);
        showToast(error.message, 'error');
    } finally {
        loading.classList.add('hidden');
    }
}

function renderTasks(tasks) {
    // Display the tasks on the page.
    taskContainer.innerHTML = '';
    emptyState.classList.toggle('hidden', tasks.length > 0);

    tasks.forEach(task => {
        const item = document.createElement('article');
        item.className = 'task-item';
        item.innerHTML = `
            <h3>${escapeHTML(task.title)}</h3>
            <p>${escapeHTML(task.description || '')}</p>
            <p>Due: ${escapeHTML(task.due_date)}</p>
            <select aria-label="Task status">
                ${['Not Started', 'In Progress', 'Completed'].map(status =>
                    `<option value="${status}" ${task.status === status ? 'selected' : ''}>${status}</option>`
                ).join('')}
            </select>
            <button type="button" class="edit-button">Edit</button>
            <button type="button" class="delete-button">Delete</button>
            <form class="edit-form hidden">
                <input type="text" name="title" value="${escapeHTML(task.title)}" required aria-label="Task title">
                <input type="date" name="due_date" value="${escapeHTML(task.due_date)}" required aria-label="Task due date">
                <textarea name="description" aria-label="Task description">${escapeHTML(task.description || '')}</textarea>
                <select name="status" aria-label="Updated task status">
                    ${['Not Started', 'In Progress', 'Completed'].map(status =>
                        `<option value="${status}" ${task.status === status ? 'selected' : ''}>${status}</option>`
                    ).join('')}
                </select>
                <button type="submit">Save changes</button>
                <button type="button" class="cancel-edit">Cancel</button>
            </form>
        `;
        item.querySelector('select').addEventListener('change', event => {
            handleStatusChange(task.id, event.target.value);
        });
        item.querySelector('.edit-button').addEventListener('click', () => {
            item.querySelector('.edit-form').classList.remove('hidden');
        });
        item.querySelector('.cancel-edit').addEventListener('click', () => {
            item.querySelector('.edit-form').classList.add('hidden');
        });
        item.querySelector('.delete-button').addEventListener('click', () => handleDeleteTask(task.id));
        item.querySelector('.edit-form').addEventListener('submit', event => {
            event.preventDefault();
            const formData = new FormData(event.target);
            updateTask(task.id, {
                title: formData.get('title').trim(),
                due_date: formData.get('due_date'),
                description: formData.get('description').trim(),
                status: formData.get('status')
            }, 'Task updated successfully.');
        });
        taskContainer.appendChild(item);
    });
}

async function handleCreateTask(event) {
    // Send a new task to the API.
    event.preventDefault();
    const dueDate = taskDueDate.value;
    if (!taskTitle.value.trim() || !dueDate) {
        showToast('Title and due date are required.', 'error');
        return;
    }

    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: taskTitle.value.trim(),
                due_date: dueDate,
                description: taskDescription.value.trim(),
                status: taskStatus.value
            })
        });
        const data = await response.json();
        if (!response.ok || !data.success) {
            throw new Error(data.message || 'Failed to create task.');
        }
        taskForm.reset();
        taskDueDate.min = new Date().toISOString().split('T')[0];
        showToast('Task created successfully.', 'success');
        fetchTasks();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function handleStatusChange(taskId, status) {
    // Update the task status.
    await updateTask(taskId, { status }, 'Task status updated successfully.');
}

async function handleDeleteTask(taskId) {
    // Delete a task from the API.
    try {
        const response = await fetch(`/api/tasks/${taskId}`, { method: 'DELETE' });
        const data = await response.json();
        if (!response.ok || !data.success) {
            throw new Error(data.message || 'Failed to delete task.');
        }
        showToast('Task deleted successfully.', 'success');
        fetchTasks();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function updateTask(taskId, changes, successMessage) {
    // Send task changes to the API.
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(changes)
        });
        const data = await response.json();
        if (!response.ok || !data.success) {
            throw new Error(data.message || 'Failed to update task.');
        }
        showToast(successMessage, 'success');
        fetchTasks();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function escapeHTML(value) {
    // Keep task text safe in the page.
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function showToast(message, type) {
    // Show a short message.
    toast.textContent = message;
    toast.className = `toast ${type}`;
    setTimeout(() => toast.classList.add('hidden'), 3000);
}