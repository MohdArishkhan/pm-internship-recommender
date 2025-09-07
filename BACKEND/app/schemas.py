from pydantic import BaseModel
from typing import List, Optional

# Education schemas
class EducationBase(BaseModel):
    description: str

class EducationCreate(EducationBase):
    pass

class Education(EducationBase):
    id: int
    
    class Config:
        from_attributes = True

# Skill schemas
class SkillBase(BaseModel):
    description: str

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    
    class Config:
        from_attributes = True

# Location schemas
class LocationBase(BaseModel):
    description: str
    state: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    
    class Config:
        from_attributes = True

# Internship schemas
class InternshipBase(BaseModel):
    title: str
    description: str
    skills_id: int
    edu_id: int
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
    location: Optional[Location] = None
    
    class Config:
        from_attributes = True

# Response schemas
class SkillsByEducationResponse(BaseModel):
    education_id: int
    education_description: str
    skills: List[Skill]

class InternshipRecommendationResponse(BaseModel):
    internships: List[Internship]
    total_count: int
