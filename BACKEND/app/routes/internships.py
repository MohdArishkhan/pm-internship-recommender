from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.crud import internship_crud
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Internship])
async def get_all_internships(db: Session = Depends(get_db)):
    # Get all available internships
    return internship_crud.get_all(db)


@router.get("/search", response_model=schemas.InternshipRecommendationResponse)
async def search_internships(
    skill_id: Optional[int] = Query(None, description="Filter by skill ID"),
    education_id: Optional[int] = Query(None, description="Filter by education ID"),
    location_id: Optional[int] = Query(None, description="Filter by location ID"),
    db: Session = Depends(get_db)
):

    # Get internships filtered by skill, education, and location
    internships = internship_crud.get_by_filters(
        db, 
        skill_id=skill_id, 
        education_id=education_id, 
        location_id=location_id
    )
    
    return schemas.InternshipRecommendationResponse(
        internships=internships,
        total_count=len(internships)
    )


