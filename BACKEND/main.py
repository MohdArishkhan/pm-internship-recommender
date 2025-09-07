from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models
from app.routes import education, location, skills, internships

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Internship Recommender API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(education.router, prefix="/api/education", tags=["education"])
app.include_router(location.router, prefix="/api/location", tags=["location"])
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
app.include_router(internships.router, prefix="/api/internships", tags=["internships"])

@app.get("/")
async def root():
    return {"message": "Internship Recommender API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
