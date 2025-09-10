# Internship Recommender Backend API

A FastAPI-based intelligent backend for an internship recommendation system with ML-enhanced scoring.

## Features

- **Smart Recommendations**: Hybrid ML + rule-based scoring system (60% rules + 40% ML)
- **Education Management**: Comprehensive education records and filtering
- **Location Management**: Location-based filtering with remote work support
- **Skills Management**: Advanced skills matching with partial similarity
- **ML Enhancement**: TF-IDF vectorization with cosine similarity for semantic matching
- **Performance Optimization**: Model caching and intelligent fallback mechanisms
- **Diversity Promotion**: Advanced algorithms to ensure recommendation diversity

## API Endpoints

### Education

- `GET /api/education/` - Get all available educations
- `GET /api/education/{id}` - Get specific education by ID

### Location

- `GET /api/location/` - Get all available locations
- `GET /api/location/{id}` - Get specific location by ID

### Skills

- `GET /api/skills/` - Get all available skills
- `GET /api/skills/{id}` - Get specific skill by ID
- `GET /api/skills/by-education/{education_id}` - Get skills filtered by education

### Internships

- `GET /api/internships/` - Get all internships
- `GET /api/internships/search` - Search internships with filters (skill_id, education_id, location_id)

### Recommendations (Core Feature)

- `POST /api/recommendations/` - Get top 5 personalized recommendations
- `POST /api/recommendations/compare` - Compare ML vs rule-based approaches
- `GET /api/recommendations/model-status` - Check ML model training status
- `POST /api/recommendations/retrain-model` - Manually retrain ML model
- `POST /api/recommendations/clear-cache` - Clear ML model cache
- `GET /api/recommendations/detailed-score/{internship_id}` - Get detailed scoring breakdown

## Setup Instructions

1. **Clone and navigate**:

   ```bash
   cd BACKEND
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
   
4. **Configure environment**:

   - Copy `.env.example` to `.env`
   - Update `DATABASE_URL` with your database credentials
   - Configure other environment variables as needed

5. **Initialize database**:

   ```bash
   python seed_data.py
   ```

6. **Start the server**:

   ```bash
   python main.py
   # or
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Train ML model** (optional for enhanced recommendations):

   ```bash
   # Access http://localhost:8000/docs
   # Use POST /api/recommendations/retrain-model endpoint
   ```

8. **Access the API**:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## ML-Enhanced Scoring System

### Hybrid Approach (60% Rules + 40% ML)

- **Rule-based scoring**: Skills matching, sector alignment, location preference, education compatibility
- **ML-based scoring**: TF-IDF vectorization with cosine similarity for semantic text matching
- **Intelligent fallback**: Automatically switches to rule-based if ML model unavailable

### Scoring Components

1. **Skills Matching** (Weight: 3) - Exact and partial skill matching with Jaccard similarity
2. **Sector Matching** (Weight: 2) - Direct and keyword-based sector alignment
3. **Location Matching** (Weight: 2) - Location preference with remote work bonus
4. **Education Matching** (Weight: 1.5) - Flexible education requirement matching
5. **Perfect Match Bonus** (Weight: 2) - Additional points for excellent matches

## Database Schema

- **Education**: Education types and degrees
- **Skill**: Technical and soft skills with comma-separated descriptions
- **Location**: Locations with state information and remote work support
- **Internship**: Complete internship details with foreign key relationships
- **Skills_Education**: Many-to-many association table for skills and education

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@host:port/database

# Application Settings
APP_NAME=Internship Recommender API
DEBUG=True
HOST=0.0.0.0
PORT=8000

# ML Model Settings
ML_MODEL_PATH=./ml_model.pkl
MODEL_CACHE_SIZE=100
```

## Project Structure

```
BACKEND/
├── app/
│   ├── __init__.py
│   ├── database.py      # Database configuration and session management
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Database operations and recommendation logic
│   ├── scoring.py       # Rule-based scoring algorithms
│   ├── ml_scoring.py    # ML-enhanced scoring with TF-IDF
│   └── routes/          # API route modules
│       ├── __init__.py
│       ├── education.py
│       ├── location.py
│       ├── skills.py
│       ├── internships.py
│       └── recommendations.py  # Core recommendation endpoints
├── main.py              # FastAPI application entry point
├── seed_data.py         # Sample data population script
├── debug_*.py          # Debugging and testing utilities
├── test_*.py           # Test suites for various components
├── .env                # Environment variables
├── .env.example        # Environment template
├── requirements.txt    # Python dependencies
├── ml_model.pkl        # Trained ML model (generated)
└── README.md           # This file
```

## Usage Examples

### Get Personalized Recommendations

```python
import requests

# Student profile
student_data = {
    "education": "Computer Science Engineering",
    "skills": ["Python", "Machine Learning", "FastAPI"],
    "sector": "Technology",
    "preferred_location": "Remote",
    "description": "Passionate about AI and web development"
}

# Get recommendations (ML-enhanced)
response = requests.post(
    "http://localhost:8000/api/recommendations/",
    json=student_data
)
recommendations = response.json()
```

### Compare Approaches

```python
# Compare ML vs rule-based recommendations
response = requests.post(
    "http://localhost:8000/api/recommendations/compare",
    json=student_data
)
comparison = response.json()
```

## Development

- **Backend Framework**: FastAPI with async support
- **Database**: MySQL with SQLAlchemy ORM
- **ML Libraries**: scikit-learn, numpy for enhanced scoring
- **Code Style**: Clean, minimal code with # comments only
- **Testing**: Comprehensive test suites for ML and scoring components

