# Task Management

A Django-based web application for managing tasks efficiently.

## Features

- Create, update, and delete tasks
- Assign due dates and priorities
- Mark tasks as complete/incomplete
- User authentication

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/abdullah149081/task-management.git
    cd task-management
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. (Optional) Create and activate a virtual environment if not already done:
    ```bash
    python -m venv task_env
    .\task_env\Scripts\activate
    ```


## Development Setup with One Command

You can start the full development environment (including Tailwind CSS watcher and Django server) using the provided PowerShell script.

### Steps to Run

1. Open PowerShell in the project root directory.

2. Run:

    ```powershell
    .\run.ps1
    ```

This script will:

- Automatically activate the Python virtual environment (`task_env`)
- Apply any pending Django migrations
- Launch the Tailwind CSS watcher in a new PowerShell window
- Start the Django development server

---

### Requirements

- Windows with PowerShell
- Python virtual environment located at `task_env` (adjust `run.ps1` if yours is different)
- Node.js and npm installed (for Tailwind CSS)

---

### Notes

- Make sure you have installed Python dependencies (`pip install -r requirements.txt`) before running the script.
- The Tailwind watcher runs in a separate window so you can watch CSS build logs.
- To stop the development server, press `Ctrl+C` in the terminal running the script.

## Usage

- Access the app at `http://127.0.0.1:8000/`
- Register or log in to manage your tasks

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

[MIT](LICENSE)
