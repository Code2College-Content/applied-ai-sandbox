# applied-ai-sandbox

Hands-on training repo for the Code2College **Applied AI Cohort** (Summer 2026
pilot). A small Flask app with intentional gaps and numbered tasks. You'll
work through tasks here using Gemini CLI as your collaborator.

This is **practice space**. Push your own branches, open PRs against
upstream — never merge straight to `main`.

## Setup

```bash
# 1. Fork this repo to your own GitHub account, then clone your fork:
git clone https://github.com/YOUR-USERNAME/applied-ai-sandbox.git
cd applied-ai-sandbox

# 2. Create a virtual environment and install deps:
python -m venv .venv
source .venv/bin/activate         # macOS/Linux
.venv\Scripts\activate            # Windows PowerShell
pip install -r requirements.txt

# 3. Run the app:
python app.py
# Open http://localhost:5000
```

## Working a task

1. Read `tasks/TASK_NN.md`.
2. Create a branch: `git checkout -b task-NN`.
3. From inside the repo, start Claude Code: `claude`.
4. Plan first — `Read tasks/TASK_NN.md and propose a plan. Don't write code yet.`
5. Implement once the plan is sound.
6. Run the tests: `pytest`.
7. Commit, push, open a PR.

## Repo layout

```
app.py                  Flask entry point (single-file app for now)
templates/              Jinja templates
tasks/                  numbered task descriptions (TASK_01.md, TASK_02.md, …)
tests/                  pytest acceptance tests for each task
GEMINI.md               project context Gemini CLI reads automatically
requirements.txt        Python dependencies
```

> **Note:** Notes you create in the running app are stored in memory and
> vanish when you restart `python app.py`. That's expected — it keeps the
> sandbox simple. Persistence is a future task.

## Ground rules

- Don't paste secrets, API keys, or personal credentials anywhere.
- Don't merge to `main` upstream.
- Stuck > 20 minutes? Ping the cohort channel.
- AI did the heavy lifting? Cool — but you should be able to explain
  every line you submit.
