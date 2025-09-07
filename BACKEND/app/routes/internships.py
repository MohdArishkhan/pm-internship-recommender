from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.crud import internship_crud
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Internship])
async def get_all_internships(db: Session = Depends(get_db)):
    """Get all available internships"""
    return internship_crud.get_all(db)

@router.get("/search", response_model=schemas.InternshipRecommendationResponse)
async def search_internships(
    skill_id: Optional[int] = Query(None, description="Filter by skill ID"),
    education_id: Optional[int] = Query(None, description="Filter by education ID"),
    location_id: Optional[int] = Query(None, description="Filter by location ID"),
    db: Session = Depends(get_db)
):
    """Get internships based on skill, education, and location filters"""
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

# @router.get("/recommend")
# async def get_internship_recommendations(
#     education_id: int = Query(..., description="Education ID for recommendations"),
#     location_id: Optional[int] = Query(None, description="Preferred location ID"),
#     db: Session = Depends(get_db)
# ):
#     """Get internship recommendations based on education and optional location preference"""
#     # Get internships that match the education
#     internships = internship_crud.get_by_filters(
#         db, 
#         education_id=education_id,
#         location_id=location_id
#     )
    
#     if not internships:
#         raise HTTPException(
#             status_code=404, 
#             detail="No internships found for the given criteria"
#         )
    
#     return schemas.InternshipRecommendationResponse(
#         internships=internships,
#         total_count=len(internships)
#     )

# @router.post("/", response_model=schemas.Internship)
# async def create_internship(internship: schemas.InternshipCreate, db: Session = Depends(get_db)):
#     """Create a new internship"""
#     return internship_crud.create(db, internship)
