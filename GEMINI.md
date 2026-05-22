# Project GEMINI: Applied AI Sandbox

This is a hands-on training repository for the **Code2College Applied AI Cohort**. It consists of a simple Flask application with intentional gaps designed to be completed through specific tasks using AI collaboration.

## Project Overview

- **Purpose:** Educational sandbox for learning AI-assisted development.
- **Technologies:** 
  - **Language:** Python 3.10+
  - **Framework:** Flask 3.0.3
  - **Testing:** pytest 8.3.3
  - **Templates:** Jinja2 with Vanilla HTML/CSS
- **Architecture:** 
  - Single-file Flask application (`app.py`) using in-memory state.
  - Task-driven structure with requirements in `tasks/` and acceptance tests in `tests/`.

## Getting Started

### Prerequisites
- Python 3.10 or higher.
- A virtual environment is recommended.

### Setup
```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
```
The app will be available at `http://localhost:5000`.

### Running Tests
```bash
# Run all tests
pytest

# Run tests for a specific task
pytest tests/test_task_NN.py
```

## Development Workflow

This project follows a strict task-based development flow:

1.  **Select a Task:** Locate the next task in the `tasks/` directory (e.g., `tasks/TASK_01.md`).
2.  **Read and Plan:** Read the task description and its corresponding test file (e.g., `tests/test_task_01.py`). Propose a plan before writing any code.
3.  **Implement:** Implement the required changes in `app.py` or the `templates/` directory.
4.  **Verify:** Run the relevant `pytest` file. The task is complete when all its acceptance tests pass.

### Key Files
- `app.py`: The main entry point and logic for the Flask app.
- `templates/`: Contains HTML files (e.g., `home.html`, `new_note.html`).
- `tasks/`: Markdown files describing the goals and acceptance criteria for each lesson.
- `tests/`: Acceptance tests that define the "done" state for each task.
- `CLAUDE.md`: Operational instructions specific to the Claude Code tool.

## Development Conventions

- **Scoped Changes:** Only modify the files necessary to complete the current task. Avoid unrelated refactoring.
- **Test Integrity:** **Never** modify the files in the `tests/` directory to make them pass. The tests are the specification.
- **In-Memory State:** For this sandbox, persistence is handled in-memory (`app.notes`). Do not add a database unless a task explicitly requires it.
- **Validation:** Always prioritize server-side validation and clear error messaging as outlined in the tasks.
