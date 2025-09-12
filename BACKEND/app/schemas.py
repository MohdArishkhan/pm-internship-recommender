from pydantic import BaseModel
from typing import List, Optional

class EducationBase(BaseModel):
    description: str

class EducationCreate(EducationBase):
    pass

class Education(EducationBase):
    id: int
    
    class Config:
        from_attributes = True

class SectorBase(BaseModel):
    name: str
    description: Optional[str] = None

class SectorCreate(SectorBase):
    pass

class Sector(SectorBase):
    id: int
    
    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    description: str

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    
    class Config:
        from_attributes = True

class LocationBase(BaseModel):
    description: str
    state: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    
    class Config:
        from_attributes = True

class InternshipBase(BaseModel):
    title: str
    description: str
    company_name: str
    skills_id: int
    edu_id: int
    sector_id: int
    location_id: int
    duration: Optional[str] = None
    no_of_post: Optional[int] = 1
    details: Optional[str] = None

class InternshipCreate(InternshipBase):
    pass

class Internship(InternshipBase):
    id: int
    skill: Optional[Skill] = None
    education: Optional[Education] = None
    sector: Optional[Sector] = None
    location: Optional[Location] = None
    
    class Config:
        from_attributes = True

class SectorsByEducationResponse(BaseModel):
    education_id: int
    education_description: str
    sectors: List[Sector]

class SkillsByEducationResponse(BaseModel):
    education_id: int
    education_description: str
    skills: List[Skill]

class SkillsBySectorResponse(BaseModel):
    sector_id: int
    sector_name: str
    skills: List[Skill]

class SkillsByEducationAndSectorResponse(BaseModel):
    education_id: int
    sector_id: int
    education_description: str
    sector_name: str
    skills: List[Skill]

class InternshipRecommendationResponse(BaseModel):
    internships: List[Internship]
    total_count: int

class StudentForm(BaseModel):
    education: str
    skills: List[str]
    sector: str
    preferred_location: str
    description: Optional[str] = ""

class RecommendationResponse(BaseModel):
    id: int
    title: str
    company_name: str
    sector: Optional[str]
    location: str
    skills: str
    duration: Optional[str]
    description: str
    match_score: float

