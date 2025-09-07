from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    
    try:
        # Create sample educations
        educations = [
            models.Education(description="Computer Science Engineering"),
            models.Education(description="Information Technology"),
            models.Education(description="Electronics and Communication"),
            models.Education(description="Mechanical Engineering"),
            models.Education(description="Business Administration")
        ]
        
        for edu in educations:
            db.add(edu)
        db.commit()
        
        # Create sample skills
        skills = [
            models.Skill(description="Python Programming"),
            models.Skill(description="Web Development"),
            models.Skill(description="Data Analysis"),
            models.Skill(description="Machine Learning"),
            models.Skill(description="Digital Marketing"),
            models.Skill(description="Project Management")
        ]
        
        for skill in skills:
            db.add(skill)
        db.commit()
        
        # Create sample locations
        locations = [
            models.Location(description="Delhi", state="Delhi"),
            models.Location(description="Mumbai", state="Maharashtra"),
            models.Location(description="Bangalore", state="Karnataka"),
            models.Location(description="Chennai", state="Tamil Nadu"),
            models.Location(description="Hyderabad", state="Telangana")
        ]
        
        for loc in locations:
            db.add(loc)
        db.commit()
        
        # Create sample internships
        internships = [
            models.Internship(
                title="Python Developer Intern",
                description="Work on backend development using Python and FastAPI",
                skills_id=1,  # Python Programming
                edu_id=1,     # Computer Science Engineering
                location_id=1, # Delhi
                duration="3 months",
                no_of_post=5,
                details="Great opportunity to learn backend development"
            ),
            models.Internship(
                title="Data Analyst Intern",
                description="Analyze data and create insights using Python and SQL",
                skills_id=3,  # Data Analysis
                edu_id=1,     # Computer Science Engineering
                location_id=3, # Bangalore
                duration="6 months",
                no_of_post=3,
                details="Work with real-world datasets"
            ),
            models.Internship(
                title="Web Development Intern",
                description="Frontend and backend web development",
                skills_id=2,  # Web Development
                edu_id=2,     # Information Technology
                location_id=2, # Mumbai
                duration="4 months",
                no_of_post=4,
                details="Build modern web applications"
            )
        ]
        
        for internship in internships:
            db.add(internship)
        db.commit()
        
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables first
    models.Base.metadata.create_all(bind=engine)
    # Then create sample data
    create_sample_data()
