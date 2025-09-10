from sqlalchemy.orm import Session
from app import models, schemas
from typing import List

class EducationCRUD:
    def get_all(self, db: Session) -> List[models.Education]:
        return db.query(models.Education).all()
    
    def get_by_id(self, db: Session, education_id: int) -> models.Education:
        return db.query(models.Education).filter(models.Education.id == education_id).first()
    
    def create(self, db: Session, education: schemas.EducationCreate) -> models.Education:
        db_education = models.Education(**education.dict())
        db.add(db_education)
        db.commit()
        db.refresh(db_education)
        return db_education


class LocationCRUD:
    def get_all(self, db: Session) -> List[models.Location]:
        return db.query(models.Location).all()
    
    def get_by_id(self, db: Session, location_id: int) -> models.Location:
        return db.query(models.Location).filter(models.Location.id == location_id).first()
    
    def create(self, db: Session, location: schemas.LocationCreate) -> models.Location:
        db_location = models.Location(**location.dict())
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return db_location


class SkillCRUD:
    def get_all(self, db: Session) -> List[models.Skill]:
        return db.query(models.Skill).all()
    
    def get_by_education_id(self, db: Session, education_id: int) -> List[models.Skill]:
        return db.query(models.Skill).join(models.skills_education).filter(
            models.skills_education.c.education_id == education_id
        ).all()
    
    def get_by_id(self, db: Session, skill_id: int) -> models.Skill:
        return db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    
    def create(self, db: Session, skill: schemas.SkillCreate) -> models.Skill:
        db_skill = models.Skill(**skill.dict())
        db.commit()
        db.refresh(db_skill)
        return db_skill


class InternshipCRUD:
    def get_all(self, db: Session) -> List[models.Internship]:
        return db.query(models.Internship).all()
    
    def get_all_with_relations(self, db: Session) -> List[models.Internship]:
        return db.query(models.Internship).options(
            db.query(models.Internship).join(models.Skill).join(models.Education).join(models.Location)
        ).all()
    
    def get_by_filters(self, db: Session, skill_id: int = None, 
                      education_id: int = None, location_id: int = None) -> List[models.Internship]:
        query = db.query(models.Internship)
        
        if skill_id:
            query = query.filter(models.Internship.skills_id == skill_id)
        if education_id:
            query = query.filter(models.Internship.edu_id == education_id)
        if location_id:
            query = query.filter(models.Internship.location_id == location_id)
            
        return query.all()
    
    def create(self, db: Session, internship: schemas.InternshipCreate) -> models.Internship:
        db_internship = models.Internship(**internship.dict())
        db.add(db_internship)
        db.commit()
        db.refresh(db_internship)
        return db_internship


def get_recommendations(db: Session, student_form: schemas.StudentForm, use_ml: bool = True) -> List[dict]:
    # Get top internship recommendations with ML or rule-based scoring
    from .scoring import calculate_total_score
    from .ml_scoring import recommendation_engine, calculate_enhanced_score, ML_AVAILABLE
    
    internships = db.query(models.Internship).all()
    
    # Check if ML model is ready
    if use_ml and ML_AVAILABLE and not recommendation_engine.is_ready_for_ml():
        print("Warning: ML model not trained. Use /retrain-model endpoint to train first.")
        use_ml = False
    
    student_data = {
        "education": student_form.education,
        "skills": student_form.skills,
        "sector": student_form.sector,
        "preferred_location": student_form.preferred_location,
        "description": student_form.description
    }
    
    # Calculate scores for each internship
    scored_internships = []
    for idx, internship in enumerate(internships):
        if use_ml and ML_AVAILABLE:
            score, score_breakdown = calculate_enhanced_score(internship, student_data, idx)
            extra_info = {"ml_enhanced": True, "score_breakdown": score_breakdown}
        else:
            score = calculate_total_score(internship, student_data)
            extra_info = {"ml_enhanced": False}
        
        if score > 0:
            scored_internships.append({
                "internship": internship,
                "score": score,
                **extra_info
            })
    
    scored_internships.sort(key=lambda x: x["score"], reverse=True)
    top_internships = scored_internships[:50]
    
    # Promote diversity by title, sector, skills, and location
    diverse_recommendations = []
    seen_titles = set()
    seen_sectors = set()
    seen_skills = set()
    seen_locations = set()
    
    # First pass: diverse recommendations
    for item in top_internships:
        internship = item["internship"]
        title = internship.title
        sector = internship.sector or "Other"
        location = internship.location.description if internship.location else "Unknown"
        skills = internship.skill.description if internship.skill else "Other"
        
        if len(diverse_recommendations) < 5:
            is_diverse = (
                skills not in seen_skills or 
                sector not in seen_sectors or 
                title not in seen_titles
            )
            
            if is_diverse:
                diverse_recommendations.append(item)
                seen_titles.add(title)
                seen_sectors.add(sector)
                seen_skills.add(skills)
                seen_locations.add(location)
    
    # Second pass: fill remaining slots
    for item in top_internships:
        if len(diverse_recommendations) >= 5:
            break
        if item not in diverse_recommendations:
            diverse_recommendations.append(item)
    
    top_5 = diverse_recommendations[:5]
    
    # Format response
    recommendations = []
    for item in top_5:
        internship = item["internship"]
        
        recommendation = {
            "id": internship.id,
            "title": internship.title,
            "sector": internship.sector or "Not specified",
            "location": internship.location.description if internship.location else "Not specified",
            "skills": internship.skill.description if internship.skill else "Not specified",
            "duration": internship.duration or "Not specified",
            "description": internship.description,
            "match_score": round(item["score"], 2)
        }
        
        # Add scoring details if ML was used
        if item.get("ml_enhanced") and item.get("score_breakdown"):
            breakdown = item["score_breakdown"]
            recommendation["scoring_details"] = {
                "ml_enhanced": True,
                "rule_based_score": round(breakdown.get("rule_based", {}).get("score", 0), 2),
                "ml_score": round(breakdown.get("ml_based", {}).get("final_score", 0), 2),
                "ml_status": breakdown.get("ml_based", {}).get("status", "unknown")
            }
        else:
            recommendation["scoring_details"] = {
                "ml_enhanced": False,
                "method": "rule_based_only"
            }
        
        recommendations.append(recommendation)
    
    return recommendations

# Create instances
education_crud = EducationCRUD()
location_crud = LocationCRUD()
skill_crud = SkillCRUD()
internship_crud = InternshipCRUD()
