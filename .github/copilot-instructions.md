# Copilot Instructions for AnyIdea? Web App

## Project Overview
- **AnyIdea?** is a web app that suggests activities based on user budget, time, preferences, location, and weather.
- **Frontend:** Vanilla HTML/CSS/JS (optionally TypeScript), no frameworks. Located in `frontend/`.
- **Backend:** Python FastAPI app in `backend/`, with business logic in `app/services/` and data models in `app/models/schemas.py`.
- **AI Integration:** Uses OpenRouter API (moonshotai/kimi-k2:free) for intelligent suggestions. WeatherAPI.com for weather data.

## Key Architectural Patterns
- **Backend** is a REST API (see `main.py`). Core endpoints: `/api/suggest`, `/api/ai-suggest`, `/health`.
- **AI and weather logic** are separated into `openrouter_service.py` and `weather_service.py`.
- **Pydantic schemas** in `schemas.py` define all request/response models. Always validate input/output against these.
- **Frontend** communicates with backend via Fetch API. No SPA framework; keep JS modular and simple.
- **No database yet** (planned: SQLite). All activity suggestions are generated on-the-fly or via AI.

## Developer Workflows
- **Backend:**
  - Activate env: `conda activate anyidea`
  - Install deps: `pip install -r requirements.txt`
  - Run: `uvicorn main:app --reload` (from `backend/`)
  - API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend:**
  - Edit HTML/CSS in `frontend/`. Use a live server for local dev.
  - Connect forms to backend endpoints using Fetch API.
- **Testing:**
  - Use `curl` or Postman to test `/api/suggest` and `/api/ai-suggest` endpoints.
  - Example request/response formats are in `README.md`.

## Project-Specific Conventions
- **All API input/output** must match the Pydantic schemas in `schemas.py`.
- **AI prompts** should include user preferences, weather, and location for best results (see prompt examples in `README.md`).
- **Frontend JS** should be modular, with clear separation between form handling, API calls, and UI updates.
- **Error handling:** Backend returns detailed error messages; frontend should display these clearly to users.
- **CORS** is enabled for frontend-backend communication.

## Integration Points
- **OpenRouter API:** Used in `openrouter_service.py` for AI suggestions. Requires API key in `.env`.
- **WeatherAPI.com:** Used in `weather_service.py` for real-time weather data.
- **Geolocation:** Frontend uses browser Geolocation API; backend expects coordinates in requests.

## Examples & References
- See `README.md` for sample API requests/responses and prompt structure.
- Key backend files: `backend/main.py`, `backend/app/services/openrouter_service.py`, `backend/app/services/weather_service.py`, `backend/app/models/schemas.py`.
- Key frontend files: `frontend/corefeatures.html`, `frontend/style/main.css`.

---

**For AI agents:**
- Always validate API changes against `schemas.py`.
- When adding new endpoints, follow FastAPI and Pydantic patterns in `main.py` and `schemas.py`.
- For new features, check the project roadmap in `README.md` to avoid duplicating planned work.
- Use clear, concise code and comments—this is a learning project for junior devs.
