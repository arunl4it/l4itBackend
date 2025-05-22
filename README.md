# FastAPI Authentication Example

This project demonstrates a simple authentication system using FastAPI, SQLAlchemy, and JWT.

## Features
- Register with email and password
- Login with email and password
- JWT-based authentication

## Setup

1. **Clone the repository** (if not already):
   ```sh
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies:**
   ```sh
   pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] python-jose[cryptography]
   ```

4. **Run the application:**
   ```sh
   uvicorn main:app --reload
   ```

5. **API Docs:**
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## Environment Variables
- `SECRET_KEY`: Set this in your environment for production security.

## Endpoints
- `POST /register` — Register a new user
- `POST /login` — Login and get JWT token

---

**Note:** This uses SQLite for demo purposes. For production, use a robust database and secure your secret keys. 