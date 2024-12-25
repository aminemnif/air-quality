# Contributing to the Django Project

This document provides essential guidelines and best practices for working collaboratively on this Django project. Follow these steps and rules to ensure a smooth workflow for everyone.

---

## ✅ Getting the Project on Your Local Machine

1. **Clone the Repository**
   - Open your terminal and run:
     ```bash
     git clone https://github.com/aminemnif/air-quality
     cd air-quality-project-deployment
     ```

2. **Set Up a Virtual Environment**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     ```bash
     venv\Scripts\activate
     ```

3. **Install Dependencies**
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run Database Migrations**
   - Apply database migrations:
     ```bash
     python manage.py migrate
     ```

5. **Run the Development Server**
   - Start the server to verify everything works:
     ```bash
     python manage.py runserver
     ```

---

## ✅ Collaboration Best Practices

### 1. **Dependency Management**

- When you add or update any Python package, run:
  ```bash
  pip freeze > requirements.txt
  ```
- Commit the updated `requirements.txt` file to ensure everyone can install the correct dependencies.

### 2. **Virtual Environment**

- Do **NOT** push your `venv/` folder to the repository.
- Ensure `venv/` is listed in the `.gitignore`.

### 3. **Git Workflow**

- Always pull the latest changes from `main` before starting work:
  ```bash
  git pull origin main
  ```
- Use feature branches for new work:
  ```bash
  git checkout -b feature/branch-name
  ```
- Commit messages should be clear and descriptive:
  ```bash
  git commit -m "Add user authentication feature"
  ```
- Push your branch and create a pull request for review:
  ```bash
  git push origin feature/branch-name
  ```

---

## 🚫 Common Pitfalls to Avoid

1. **Don’t Push Personal Configurations**\
   Avoid pushing files like `.env`, `settings.py` with hardcoded credentials, or editor-specific files (e.g., `.vscode/`, `.idea/`).

2. **Avoid Conflicts with Migrations**

   - Run migrations locally before pushing.
   - If you create new migrations, ensure they don’t conflict with existing ones.

3. **Don’t Ignore ****`.gitignore`**\
   Double-check that your `.gitignore` is respected to avoid unnecessary files in the repository.

4. **Don’t Work Directly on ****`main`**\
   Always create a new branch for your work and submit a pull request.