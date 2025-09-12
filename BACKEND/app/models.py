from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Many-to-many association table for education and sectors
education_sectors = Table(
    'education_sectors',
    Base.metadata,
    Column('education_id', Integer, ForeignKey('educations.id')),
    Column('sector_id', Integer, ForeignKey('sectors.id'))
)

# Many-to-many association table for sectors and skills
sector_skills = Table(
    'sector_skills',
    Base.metadata,
    Column('sector_id', Integer, ForeignKey('sectors.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

class Education(Base):
    __tablename__ = "educations"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    
    sectors = relationship("Sector", secondary=education_sectors, back_populates="educations")

class Sector(Base):
    __tablename__ = "sectors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    educations = relationship("Education", secondary=education_sectors, back_populates="sectors")
    skills = relationship("Skill", secondary=sector_skills, back_populates="sectors")
    internships = relationship("Internship", back_populates="sector")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    
    sectors = relationship("Sector", secondary=sector_skills, back_populates="skills")
    internships = relationship("Internship", back_populates="skill")

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    state = Column(String(100), nullable=True)
    
    internships = relationship("Internship", back_populates="location")

class Internship(Base):
    __tablename__ = "internships"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    company_name = Column(String(200), nullable=False, index=True)
    skills_id = Column(Integer, ForeignKey('skills.id'), index=True)
    edu_id = Column(Integer, ForeignKey('educations.id'), index=True)
    sector_id = Column(Integer, ForeignKey('sectors.id'), index=True)
    location_id = Column(Integer, ForeignKey('locations.id'), index=True)
    duration = Column(String(50), nullable=True, index=True)
    no_of_post = Column(Integer, default=1)
    details = Column(Text, nullable=True)
    
    skill = relationship("Skill", back_populates="internships")
    education = relationship("Education")
    sector = relationship("Sector", back_populates="internships")
    location = relationship("Location", back_populates="internships")
