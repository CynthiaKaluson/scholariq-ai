# Contributing to Scholariq-AI

Thank you for your interest in contributing to Scholariq-AI.

This project explores reliable AI-assisted academic writing by combining content generation with automated citation validation. Contributions that improve stability, code quality, testing, or documentation are welcome.

---

# Ways to Contribute

There are several ways to help improve the project.

### Report Bugs

If you encounter a bug, open a GitHub Issue and include:

* a clear description of the problem
* steps to reproduce it
* expected vs actual behavior
* relevant logs or error messages

This helps maintainers diagnose the issue quickly.

---

### Suggest Improvements

Ideas for improving the API, architecture, validation logic, or documentation are welcome.

Before submitting large feature proposals, please open an Issue to discuss the idea first.

This helps prevent duplicated work.

---

### Submit Code Changes

Pull requests are encouraged for:

* bug fixes
* performance improvements
* improved validation logic
* documentation improvements
* additional tests

Please keep pull requests focused on a single change.

---

# Development Setup

Clone the repository.

```bash
git clone https://github.com/CynthiaKaluson/scholariq-ai.git
cd scholariq-ai
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the development server.

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

Interactive documentation is available at:

```
http://localhost:8000/docs
```

---

# Project Structure Overview

```
app/
  routes/      API endpoints
  services/    AI generation and validation logic
  models/      request and response schemas
  core/        configuration, authentication, rate limiting
  tests/       automated tests
```

Keeping these responsibilities separate helps maintain readability and maintainability.

---

# Code Style Guidelines

To keep the codebase consistent:

* Use clear and descriptive variable names
* Keep functions focused on a single responsibility
* Follow existing project structure
* Add docstrings to important modules or services

When modifying existing files, follow the style already used in that file.

---

# Testing

If you add new functionality, please include relevant tests inside the `tests/` directory.

Testing helps prevent regressions and improves reliability of the API.

---

# Pull Request Process

1. Fork the repository
2. Create a new branch for your change

```
git checkout -b feature/my-feature
```

3. Commit your changes with clear messages

```
git commit -m "Add citation validation improvement"
```

4. Push your branch

```
git push origin feature/my-feature
```

5. Open a Pull Request on GitHub

Please include a short explanation of the change and why it is needed.

---

# Code of Conduct

Contributors are expected to communicate respectfully and constructively.

The goal of the project is to encourage learning, experimentation, and collaboration around reliable AI-assisted writing systems.

---

Thank you for helping improve Scholariq-AI.
