# GAC API

Backend API for Gemini Admin Console (GAC).

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   Copy `.env.example` to `.env` and adjust if necessary.

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Documentation

- Swagger UI: `/docs`
- ReDoc: `/redoc`
