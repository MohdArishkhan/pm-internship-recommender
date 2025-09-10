from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import location_crud
from app import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Location])
async def get_all_locations(db: Session = Depends(get_db)):
    # Get all available locations
    return location_crud.get_all(db)


@router.get("/{location_id}", response_model=schemas.Location)
async def get_location(location_id: int, db: Session = Depends(get_db)):

    # Get specific location by ID
    location = location_crud.get_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


