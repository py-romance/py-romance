#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import time

BASE_DIR = "ukubona_world"
VENV_DIR = "myenv"
FLASK_APP = "app.py"
REQUIREMENTS = [
    "flask",
    "pyyaml",
]

# Directory structure to create
DIR_STRUCTURE = [
    "agents/friends",
    "agents/foes",
    "agents/others",
    "events/shocks",
    "events/environmental",
    "logs",
    "templates",
    "static/css",
    "static/js",
    "config",
]

# Files to populate (path relative to BASE_DIR)
FILES_CONTENT = {
    "README.md": "# Ukubona Recursive Intelligence System\n\nThis repo bootstraps Ukubona's recursive simulation and Flask API.\n",
    ".gitignore": """
myenv/
__pycache__/
*.pyc
ukubona_world/
""",
    "requirements.txt": "\n".join(REQUIREMENTS) + "\n",
    "config/render.yaml": """\
type: web
env: python
buildCommand: ./{venv}/bin/pip install -r requirements.txt
startCommand: ./{venv}/bin/python {app}
""".format(venv=VENV_DIR, app=FLASK_APP),
    FLASK_APP: '''\
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.jinja2")

if __name__ == "__main__":
    app.run(debug=True)
''',
    "templates/index.jinja2": '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Ukubona Recursive Intelligence</title>
    <link rel="stylesheet" href="/static/css/style.css" />
</head>
<body>
    <h1>Welcome to Ukubona LLC</h1>
    <p>The recursive intelligence system is bootstrapped.</p>
</body>
</html>
''',
    "static/css/style.css": '''\
body {
    font-family: Arial, sans-serif;
    margin: 3em;
    background-color: #f0f4f8;
    color: #222;
}
h1 {
    color: #0077cc;
}
''',
}

def run(cmd, check=True, shell=False):
    print(f">>> Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, check=check, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        print(result.stdout.decode())
    if result.stderr:
        print(result.stderr.decode())
    return result

def create_directories():
    if os.path.exists(BASE_DIR):
        print(f"Removing existing directory {BASE_DIR} ...")
        shutil.rmtree(BASE_DIR)
    print(f"Creating base directory {BASE_DIR} ...")
    os.makedirs(BASE_DIR)
    for d in DIR_STRUCTURE:
        path = os.path.join(BASE_DIR, d)
        os.makedirs(path, exist_ok=True)
        readme_path = os.path.join(path, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, "w") as f:
                f.write(f"# Directory: {d}\n")
    print("Directories created.\n")

def write_files():
    for filepath, content in FILES_CONTENT.items():
        full_path = os.path.join(BASE_DIR, filepath)
        dirname = os.path.dirname(full_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(full_path, "w") as f:
            f.write(content)
        print(f"Created {filepath}")
    print("All files written.\n")

def create_venv_and_install():
    venv_path = os.path.join(BASE_DIR, VENV_DIR)
    if os.path.exists(venv_path):
        print(f"Removing existing virtual environment at {venv_path} ...")
        shutil.rmtree(venv_path)
    print(f"Creating virtual environment at {venv_path} ...")
    run([sys.executable, "-m", "venv", venv_path])
    pip_path = os.path.join(venv_path, "bin", "pip")
    print("Installing requirements in virtual environment ...")
    run([pip_path, "install"] + REQUIREMENTS)
    print("Virtual environment ready.\n")

def launch_flask():
    venv_bin = os.path.join(BASE_DIR, VENV_DIR, "bin")
    python_path = os.path.join(venv_bin, "python")
    app_path = os.path.join(BASE_DIR, FLASK_APP)
    print("Launching Flask app (press Ctrl+C to exit)...")
    subprocess.run([python_path, app_path])

def git_init_and_push():
    cwd = os.getcwd()
    os.chdir(BASE_DIR)
    if not os.path.exists(".git"):
        print("Initializing git repository ...")
        run(["git", "init"])
    else:
        print("Git repository already exists.")
    print("Adding files and committing ...")
    run(["git", "add", "."])
    run(["git", "commit", "-m", "Initial recursive origins commit"])
    print("Pushing to origin (make sure remote is set)...")
    try:
        run(["git", "push", "-u", "origin", "main"])
    except Exception as e:
        print("Push failed. Make sure git remote 'origin' is configured and you have permissions.")
    os.chdir(cwd)
    print("Git push complete.\n")

def main():
    print("\n🌀 Ukubona Origins Bootstrapper Starting...\n")
    create_directories()
    write_files()
    create_venv_and_install()
    git_init_and_push()
    launch_flask()
    print("\n✅ Ukubona Origins Complete\n")

if __name__ == "__main__":
    main()