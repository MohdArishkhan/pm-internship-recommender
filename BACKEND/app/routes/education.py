from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import education_crud
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Education])
async def get_all_educations(db: Session = Depends(get_db)):
    # Get all available educations
    return education_crud.get_all(db)


@router.get("/{education_id}", response_model=schemas.Education)
async def get_education(education_id: int, db: Session = Depends(get_db)):

    # Get specific education by ID
    education = education_crud.get_by_id(db, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    return education


