# AI-OS Backend
# AI-OS Backend

## Features
- Production-ready FastAPI backend
- JWT authentication, organization management, file storage, networking, firewall, quota, audit log, legal hold
- Postgres database with SQLAlchemy ORM and Alembic migrations

## Setup

1. Copy `.env` and fill in your secrets, database credentials, and mail server info.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run Alembic migrations:
    ```bash
    alembic upgrade head
    ```
4. Start the server:
    ```bash
    uvicorn app.main:app --reload
    ```

## Docker

```bash
docker build -t ai-os-backend .
docker run -p 8000:8000 --env-file .env ai-os-backend
```

## API Docs

Visit `http://localhost:8000/docs` after running the server.

A production-ready backend for a modern "AI-OS" system, built with FastAPI, SQLAlchemy, JWT, file storage, user management, network/system control, and more.

## Features

- User authentication (JWT)
- User, file, network, firewall CRUD
- File storage (local or S3)
- Admin system/network/terminal control
- Email password reset
- Alembic migrations
- RESTful API

## Quickstart

1. **Clone and Install**

   ```bash
   git clone https://your-repo-url
   cd ai-os-backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure**

   - Copy `.env` and edit for your environment.

3. **Database migration**

   ```bash
   alembic upgrade head
   ```

4. **Run**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **API Docs**

   - Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Production Tips

- Use `uvicorn` behind `gunicorn` or similar for production.
- Set strong `SECRET_KEY` and configure DB, S3, email properly.
- Use HTTPS in production.
- Restrict CORS origins.
- Set up logging, monitoring, and error reporting.
- Regularly update dependencies.

## Advanced

- Add test suite (pytest).
- Extend models and endpoints as needed.
- Integrate with your frontend.

---

© 2025 Your Team
