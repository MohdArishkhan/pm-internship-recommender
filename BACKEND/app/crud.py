from sqlalchemy.orm import Session
from app import models, schemas
from typing import List
import hashlib
import json
from datetime import datetime, timedelta

# Simple in-memory cache for recommendations
recommendation_cache = {}
cache_ttl = 300  # 5 minutes cache

def get_cache_key(student_form: schemas.StudentForm, use_ml: bool) -> str:
    """Generate cache key from student form data"""
    form_data = {
        "education": student_form.education,
        "skills": sorted(student_form.skills) if student_form.skills else [],
        "sector": student_form.sector,
        "preferred_location": student_form.preferred_location,
        "description": student_form.description,
        "use_ml": use_ml
    }
    return hashlib.md5(json.dumps(form_data, sort_keys=True).encode()).hexdigest()


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


class SectorCRUD:
    def get_all(self, db: Session) -> List[models.Sector]:
        return db.query(models.Sector).all()
    
    def get_by_id(self, db: Session, sector_id: int) -> models.Sector:
        return db.query(models.Sector).filter(models.Sector.id == sector_id).first()
    
    def get_by_education_id(self, db: Session, education_id: int) -> List[models.Sector]:
        return db.query(models.Sector).join(models.education_sectors).filter(
            models.education_sectors.c.education_id == education_id
        ).all()
    
    def create(self, db: Session, sector: schemas.SectorCreate) -> models.Sector:
        db_sector = models.Sector(**sector.dict())
        db.add(db_sector)
        db.commit()
        db.refresh(db_sector)
        return db_sector


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
        # Get skills through education -> sectors -> skills relationship
        return db.query(models.Skill).join(models.sector_skills).join(models.education_sectors).filter(
            models.education_sectors.c.education_id == education_id
        ).distinct().all()
    
    def get_by_sector_id(self, db: Session, sector_id: int) -> List[models.Skill]:
        return db.query(models.Skill).join(models.sector_skills).filter(
            models.sector_skills.c.sector_id == sector_id
        ).all()
    
    def get_by_education_and_sector(self, db: Session, education_id: int, sector_id: int) -> List[models.Skill]:
        # Get skills that belong to a specific sector, and that sector is associated with the education
        return db.query(models.Skill).join(models.sector_skills).join(models.education_sectors).filter(
            models.sector_skills.c.sector_id == sector_id,
            models.education_sectors.c.education_id == education_id,
            models.education_sectors.c.sector_id == sector_id
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


def extract_multiple_skills(internship, db_session=None):
    """Extract multiple skills from internship, including both primary skill and additional skills from details"""
    skills = []
    
    # Add primary skill
    if internship.skill:
        skills.append(internship.skill.description)
    
    # Extract additional skills from details field
    if internship.details and "Additional_Skills_IDs:" in internship.details:
        try:
            additional_part = internship.details.split("Additional_Skills_IDs:")[1].split("This")[0]
            skill_ids = [int(x.strip()) for x in additional_part.split(",") if x.strip().isdigit()]
            
            # Use provided session to avoid creating new connections
            if db_session and skill_ids:
                additional_skills = db_session.query(models.Skill).filter(
                    models.Skill.id.in_(skill_ids)
                ).all()
                for skill in additional_skills:
                    skills.append(skill.description)
        except:
            pass  # If parsing fails, just use primary skill
    
    return skills

def get_recommendations(db: Session, student_form: schemas.StudentForm, use_ml: bool = True) -> List[dict]:
    # Check cache first
    cache_key = get_cache_key(student_form, use_ml)
    cached_result = recommendation_cache.get(cache_key)
    
    if cached_result:
        cache_time, cached_recommendations = cached_result
        if datetime.now() - cache_time < timedelta(seconds=cache_ttl):
            print("🚀 Returning cached recommendations")
            return cached_recommendations
        else:
            # Remove expired cache entry
            del recommendation_cache[cache_key]
    
    # Get top internship recommendations with ML or rule-based scoring
    from .scoring import calculate_total_score
    from .ml_scoring import recommendation_engine, calculate_enhanced_score, ML_AVAILABLE
    
    # Pre-filter internships based on user preferences for better performance
    from sqlalchemy.orm import joinedload
    
    query = db.query(models.Internship).options(
        joinedload(models.Internship.sector),
        joinedload(models.Internship.location),
        joinedload(models.Internship.skill),
        joinedload(models.Internship.education)
    )
    
    # Filter by sector if specified
    if student_form.sector and student_form.sector != "Any":
        query = query.join(models.Sector).filter(models.Sector.name.ilike(f"%{student_form.sector}%"))
    
    # Filter by location if specified
    if student_form.preferred_location and student_form.preferred_location != "Any":
        query = query.join(models.Location).filter(models.Location.description.ilike(f"%{student_form.preferred_location}%"))
    
    # Limit initial results for performance (we'll score these and pick top 50)
    internships = query.limit(1000).all()
    
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
    
    # Calculate scores for each internship (optimized with early filtering)
    scored_internships = []
    min_score_threshold = 10  # Only consider internships with score > 10
    
    for idx, internship in enumerate(internships):
        # Quick pre-filter: check if any user skills match internship skills
        internship_skills = extract_multiple_skills(internship, db)
        if student_form.skills:
            skill_match = any(skill.lower() in ' '.join(internship_skills).lower() 
                            for skill in student_form.skills)
            if not skill_match and internship.sector.name.lower() not in student_form.sector.lower():
                continue  # Skip internships with no skill or sector match
        
        if use_ml and ML_AVAILABLE:
            score, score_breakdown = calculate_enhanced_score(internship, student_data, idx)
            extra_info = {"ml_enhanced": True, "score_breakdown": score_breakdown}
        else:
            score = calculate_total_score(internship, student_data)
            extra_info = {"ml_enhanced": False}
        
        # Only add internships with meaningful scores
        if score > min_score_threshold:
            scored_internships.append({
                "internship": internship,
                "score": score,
                "skills": internship_skills,  # Cache extracted skills
                **extra_info
            })
            
        # Early termination: if we have enough high-scoring internships, stop
        if len(scored_internships) >= 100:
            break
    
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
        sector = internship.sector.name if internship.sector else "Other"
        location = internship.location.description if internship.location else "Unknown"
        skills = ", ".join(item["skills"]) if item.get("skills") else (internship.skill.description if internship.skill else "Other")
        
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
        
        # Use cached skills from scoring phase for better performance
        if item.get("skills"):
            all_skills_text = ", ".join(item["skills"])
        else:
            all_skills_text = internship.skill.description if internship.skill else "Not specified"
 
        recommendation = {
            "id": internship.id,
            "title": internship.title,
            "company_name": internship.company_name,
            "sector": internship.sector.name if internship.sector else "Not specified",
            "location": internship.location.description if internship.location else "Not specified",
            "skills": all_skills_text,
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
    
    # Cache the results for future requests
    recommendation_cache[cache_key] = (datetime.now(), recommendations)
    
    # Clean up old cache entries (keep only last 100 entries)
    if len(recommendation_cache) > 100:
        oldest_key = min(recommendation_cache.keys(), 
                        key=lambda k: recommendation_cache[k][0])
        del recommendation_cache[oldest_key]
    
    print(f"🎯 Generated {len(recommendations)} recommendations (cached for {cache_ttl}s)")
    return recommendations


# Create instances
education_crud = EducationCRUD()
sector_crud = SectorCRUD()
location_crud = LocationCRUD()
skill_crud = SkillCRUD()
internship_crud = InternshipCRUD()
