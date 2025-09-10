from typing import List, Dict
from .models import Internship

# Scoring weights
SKILL_MATCH_WEIGHT = 3
SECTOR_MATCH_WEIGHT = 2
LOCATION_MATCH_WEIGHT = 1
EDUCATION_MATCH_WEIGHT = 1.5
PERFECT_MATCH_BONUS = 2

# Education hierarchy (higher index = higher qualification)
EDUCATION_HIERARCHY = {
    "10th Pass": 0,
    "12th Pass": 1,
    "Diploma": 2,
    "Bachelor's": 3,
    "Master's": 4,
    "PhD": 5
}

def calculate_rule_based_score(internship: Internship, student_data: Dict) -> float:
    """
    Calculate score based on rules (60% weightage in final score)
    """
    score = 0
    max_possible_score = 0
    
    # 1. Skills matching (weight: 3)
    internship_skills = set(skill.strip().lower() for skill in internship.skill.description.split(',')) if internship.skill else set()
    student_skills = set(skill.strip().lower() for skill in student_data['skills'])
    
    if internship_skills and student_skills:
        skill_match_ratio = len(internship_skills.intersection(student_skills)) / len(internship_skills)
        score += skill_match_ratio * SKILL_MATCH_WEIGHT
    max_possible_score += SKILL_MATCH_WEIGHT
    
    # 2. Sector matching (weight: 2)
    if internship.sector and internship.sector.lower() == student_data['sector'].lower():
        score += SECTOR_MATCH_WEIGHT
    max_possible_score += SECTOR_MATCH_WEIGHT
    
    # 3. Location matching (weight: 1)
    if internship.location and internship.location.description.lower() == student_data['preferred_location'].lower():
        score += LOCATION_MATCH_WEIGHT
    # Partial score for "Remote" internships
    elif internship.location and internship.location.description.lower() == "remote":
        score += LOCATION_MATCH_WEIGHT * 0.5
    max_possible_score += LOCATION_MATCH_WEIGHT
    
    # 4. Education matching (weight: 1.5)
    student_edu_level = EDUCATION_HIERARCHY.get(student_data['education'], 0)
    required_edu_level = EDUCATION_HIERARCHY.get(internship.education.description if internship.education else "", 0)
    
    if student_edu_level >= required_edu_level:
        score += EDUCATION_MATCH_WEIGHT
    elif student_edu_level == required_edu_level - 1:
        # Partial score if just one level below
        score += EDUCATION_MATCH_WEIGHT * 0.5
    max_possible_score += EDUCATION_MATCH_WEIGHT
    
    # 5. Perfect match bonus
    skill_match_ratio = len(internship_skills.intersection(student_skills)) / len(internship_skills) if internship_skills else 0
    if (skill_match_ratio >= 0.8 and 
        internship.sector and internship.sector.lower() == student_data['sector'].lower() and
        internship.location and internship.location.description.lower() == student_data['preferred_location'].lower() and
        student_edu_level >= required_edu_level):
        score += PERFECT_MATCH_BONUS
    max_possible_score += PERFECT_MATCH_BONUS
    
    # Normalize to 0-60 (60% weightage)
    normalized_score = (score / max_possible_score) * 60 if max_possible_score > 0 else 0
    
    return normalized_score

def calculate_description_similarity_mock(internship_desc: str, student_desc: str) -> float:
    """
    Mock function for description similarity (ML part - 40% weightage)
    In production, this would use NLP/ML techniques
    For now, using simple keyword matching as placeholder
    """
    if not internship_desc or not student_desc:
        return 0
    
    # Simple keyword matching (placeholder for ML)
    internship_words = set(internship_desc.lower().split())
    student_words = set(student_desc.lower().split())
    
    # Remove common stop words
    stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'as', 'are', 'was', 'were', 'to', 'in', 'for', 'of', 'with', 'by'}
    internship_words -= stop_words
    student_words -= stop_words
    
    if not internship_words or not student_words:
        return 0
    
    # Calculate Jaccard similarity
    intersection = len(internship_words.intersection(student_words))
    union = len(internship_words.union(student_words))
    
    similarity = (intersection / union) if union > 0 else 0
    
    # Return score out of 40 (40% weightage)
    return similarity * 40

def calculate_total_score(internship: Internship, student_data: Dict) -> float:
    """
    Calculate total score combining rule-based (60%) and description similarity (40%)
    """
    rule_score = calculate_rule_based_score(internship, student_data)
    
    # Mock ML score - in production, this would call actual ML model
    ml_score = calculate_description_similarity_mock(
        internship.description, 
        student_data.get('description', '')
    )
    
    total_score = rule_score + ml_score
    
    return min(total_score, 100)
