# Internship Recommender Backend API

A FastAPI-based backend for an internship recommendation system.

## Features

- **Education Management**: Get and create education records
- **Location Management**: Get and create location records
- **Skills Management**: Get skills and filter by education
- **Internship Recommendations**: Get internships based on education, skills, and location

## API Endpoints

### Education

- `GET /api/education/` - Get all educations
- `GET /api/education/{id}` - Get specific education
- `POST /api/education/` - Create new education

### Location

- `GET /api/location/` - Get all locations
- `GET /api/location/{id}` - Get specific location
- `POST /api/location/` - Create new location

### Skills

- `GET /api/skills/` - Get all skills
- `GET /api/skills/{id}` - Get specific skill
- `GET /api/skills/by-education/{education_id}` - Get skills by education
- `POST /api/skills/` - Create new skill

### Internships

- `GET /api/internships/` - Get all internships
- `GET /api/internships/search?skill_id=1&education_id=2&location_id=3` - Search internships
- `GET /api/internships/recommend?education_id=1&location_id=2` - Get recommendations
- `POST /api/internships/` - Create new internship

## Setup Instructions

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database**:

   - Update the `DATABASE_URL` in `.env` file with your actual password
   - The current URL is configured for TiDB Cloud

3. **Run the application**:

   ```bash
   python run.py
   ```

   Or directly:

   ```bash
   uvicorn main:app --reload
   ```

4. **Create sample data** (optional):

   ```bash
   python seed_data.py
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Database Schema

The application uses the following models:

- **Education**: Store education types/degrees
- **Skill**: Store various skills
- **Location**: Store locations with state information
- **Internship**: Store internship details with relationships to skills, education, and location
- **Skills_Education**: Many-to-many relationship between skills and education

## Environment Variables

Create a `.env` file with:

```
DATABASE_URL=mysql+pymysql://username:password@host:port/database
APP_NAME=Internship Recommender API
DEBUG=True
```

## Project Structure

```
BACKEND/
├── app/
│   ├── __init__.py
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   └── routes/          # API routes
│       ├── __init__.py
│       ├── education.py
│       ├── location.py
│       ├── skills.py
│       └── internships.py
├── main.py              # FastAPI application
├── run.py               # Application runner
├── seed_data.py         # Sample data creation
├── .env                 # Environment variables
└── requirements.txt     # Dependencies
```
