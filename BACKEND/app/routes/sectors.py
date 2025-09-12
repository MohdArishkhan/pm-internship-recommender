from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import sector_crud, education_crud
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Sector])
async def get_all_sectors(db: Session = Depends(get_db)):
    # Get all available sectors
    return sector_crud.get_all(db)


# @router.get("/{sector_id}", response_model=schemas.Sector)
# async def get_sector(sector_id: int, db: Session = Depends(get_db)):
#     # Get specific sector by ID
#     sector = sector_crud.get_by_id(db, sector_id)
#     if not sector:
#         raise HTTPException(status_code=404, detail="Sector not found")
#     return sector


@router.get("/by-education/{education_id}", response_model=schemas.SectorsByEducationResponse)
async def get_sectors_by_education(education_id: int, db: Session = Depends(get_db)):
    # Get sectors based on education ID
    education = education_crud.get_by_id(db, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    
    sectors = sector_crud.get_by_education_id(db, education_id)
    
    return schemas.SectorsByEducationResponse(
        education_id=education_id,
        education_description=education.description,
        sectors=sectors
    )
