from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import skill_crud, education_crud
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Skill])
async def get_all_skills(db: Session = Depends(get_db)):
    """Get all available skills"""
    return skill_crud.get_all(db)


@router.get("/by-education/{education_id}", response_model=schemas.SkillsByEducationResponse)
async def get_skills_by_education(education_id: int, db: Session = Depends(get_db)):
    """Get skills based on education ID"""
    education = education_crud.get_by_id(db, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    
    skills = skill_crud.get_by_education_id(db, education_id)
    
    return schemas.SkillsByEducationResponse(
        education_id=education_id,
        education_description=education.description,
        skills=skills
    )


@router.get("/{skill_id}", response_model=schemas.Skill)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """Get a specific skill by ID"""
    skill = skill_crud.get_by_id(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


# @router.post("/", response_model=schemas.Skill)
# async def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
#     """Create a new skill"""
#     return skill_crud.create(db, skill)
