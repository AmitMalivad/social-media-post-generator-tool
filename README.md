# Social Media Post Generator Tool

Generate platform-ready social media posts (Instagram, LinkedIn, Facebook) with AI. The tool saves project and generated-post data to PostgreSQL and uses the Gemini API for content generation.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Google Gemini API
- **Frontend:** HTML, CSS, JavaScript (vanilla)

---

## Prerequisites

- **Python 3.10+**
- **PostgreSQL** (installed and running)
- **Google Gemini API key** ([Get one here](https://aistudio.google.com/apikey))

---

## Project Structure

```
social-media-post-generator-tool/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── content.py      # Content API routes
│   │   ├── core/
│   │   │   ├── database.py     # DB models & connection
│   │   │   └── gemini.py       # Gemini API integration
│   │   ├── schemas/
│   │   │   └── content.py      # Request/response models
│   │   └── main.py             # FastAPI app
│   ├── requirements.txt
│   └── (optional) .env         # GEMINI_API_KEY, DATABASE_URL
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md
```

---

## Setup & Run

### Step 1: Clone and enter the project

```bash
cd social-media-post-generator-tool
```

### Step 2: Set up PostgreSQL

1. Install PostgreSQL if needed ([download](https://www.postgresql.org/download/)).
2. Create a database, for example:

   ```bash
   # Using psql (replace with your postgres user if different)
   psql -U postgres -c "CREATE DATABASE social_media;"
   ```

3. Note your connection details: **user**, **password**, **host**, **port** (default `5432`), **database name**.

### Step 3: Backend setup

1. Go to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   ```

   - **Windows (Command Prompt):** `venv\Scripts\activate`
   - **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
   - **macOS/Linux:** `source venv/bin/activate`

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in `backend/app/` (or in `backend/`) with your API key and database URL:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/social_media
   ```

   Replace `USER`, `PASSWORD`, and `social_media` with your PostgreSQL credentials and database name.  
   If you omit `DATABASE_URL`, the app defaults to:

   `postgresql://admin:admin@localhost:5432/social_media`

5. Run the API server:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be at **http://localhost:8000**.  
   Tables `projects` and `generated_posts` are created automatically on startup.

### Step 4: Frontend setup

1. Open a **new terminal** (keep the backend running in the first one).

2. Serve the frontend. From the project root:

   **Option A – Python HTTP server (recommended):**

   ```bash
   cd frontend
   python -m http.server 5500
   ```

   Then open: **http://localhost:5500**

   **Option B – Open file directly:**

   Open `frontend/index.html` in your browser (e.g. double-click or drag into Chrome).  
   If the API is on `http://localhost:8000`, the frontend will work. For other hosts/ports, edit `API_BASE` in `frontend/app.js`.

### Step 5: Use the app

1. In the web UI, fill in:
   - Business name, industry, target audience, location
   - Business goal, tone, number of posts (1–30)
2. Click **Generate posts**.
3. After generation, each post shows:
   - Caption (platform-neutral)
   - Platform variations (Instagram, LinkedIn, Facebook)
   - Hashtags, CTA
   - Creative suggestion (type, overlay, color theme)
   - Image prompt (for DALL·E / Midjourney / Stable Diffusion)

---

## API Reference

- **Base URL:** `http://localhost:8000`
- **Generate content:** `POST /api/v1/content/`

**Request body (JSON):**

```json
{
  "business_name": "string",
  "industry": "string",
  "target_audience": "string",
  "location": "string",
  "business_goal": "Leads" | "Branding" | "Sales" | "Engagement",
  "tone": "Professional" | "Friendly" | "Bold" | "Educational",
  "number_of_posts": 1
}
```

**Response:** JSON with `business_name` and `generated_posts` (array of posts with caption, platform variations, hashtags, cta, creative fields, and `ai_image_prompt`).

Interactive docs: **http://localhost:8000/docs**

---

## Troubleshooting

| Issue | What to do |
|--------|------------|
| `GEMINI_API_KEY not found` | Add `GEMINI_API_KEY` to `backend/app/.env` (or `backend/.env`) and restart the server. |
| Database connection error | Check PostgreSQL is running, and that `DATABASE_URL` user/password/database name are correct. |
| CORS or “Failed to fetch” | Ensure the backend is running at the URL used in `frontend/app.js` (default `http://localhost:8000`). CORS is enabled for all origins. |
| Frontend shows error | Confirm backend is running and reachable at `http://localhost:8000`. |

---

## License

Use as needed for your assignment or project.
