from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, crud

router = APIRouter()

@router.post("/", response_model=List[schemas.RecommendationResponse])
def get_recommendations(
    student_form: schemas.StudentForm,
    db: Session = Depends(get_db)
):
    """
    Get top 5 internship recommendations based on student profile
    """
    recommendations = crud.get_recommendations(db, student_form)
    
    if not recommendations:
        raise HTTPException(
            status_code=404, 
            detail="No matching internships found for your profile"
        )
    
    return recommendations
