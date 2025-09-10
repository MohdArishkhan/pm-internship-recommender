from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Many-to-many association table for skills and education
skills_education = Table(
    'skills_education',
    Base.metadata,
    Column('skill_id', Integer, ForeignKey('skills.id')),
    Column('education_id', Integer, ForeignKey('educations.id'))
)


class Education(Base):
    __tablename__ = "educations"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    
    # Relationships
    skills = relationship("Skill", secondary=skills_education, back_populates="educations")


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    
    # Relationships
    educations = relationship("Education", secondary=skills_education, back_populates="skills")
    internships = relationship("Internship", back_populates="skill")


class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    state = Column(String(100), nullable=True)
    
    # Relationships
    internships = relationship("Internship", back_populates="location")


class Internship(Base):
    __tablename__ = "internships"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    skills_id = Column(Integer, ForeignKey('skills.id'))
    edu_id = Column(Integer, ForeignKey('educations.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    duration = Column(String(50), nullable=True)
    no_of_post = Column(Integer, default=1)
    details = Column(Text, nullable=True)
    sector = Column(String(100), nullable=True)

    # Relationships
    skill = relationship("Skill", back_populates="internships")
    education = relationship("Education")
    location = relationship("Location", back_populates="internships")
