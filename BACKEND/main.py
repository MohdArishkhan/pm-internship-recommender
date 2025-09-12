import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import education, location, skills, internships, recommendations, sectors

app = FastAPI(title="Internship Recommender API", version="1.0.0")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(education.router, prefix="/api/education", tags=["education"])
app.include_router(location.router, prefix="/api/location", tags=["location"])
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
app.include_router(sectors.router, prefix="/api/sectors", tags=["sectors"])
app.include_router(internships.router, prefix="/api/internships", tags=["internships"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])

@app.get("/")
async def root():
    return {"message": "Internship Recommender API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

