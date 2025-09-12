from typing import Dict
from .models import Internship

# Scoring weights
SKILL_MATCH_WEIGHT = 3
SECTOR_MATCH_WEIGHT = 2
LOCATION_MATCH_WEIGHT = 2
EDUCATION_MATCH_WEIGHT = 1.5
PERFECT_MATCH_BONUS = 2

# Education hierarchy
EDUCATION_HIERARCHY = {
    "10th Pass": 0,
    "12th Pass": 1,
    "Diploma": 2,
    "Bachelor's": 3,
    "Master's": 4,
    "PhD": 5
}

def calculate_rule_based_score(internship: Internship, student_data: Dict) -> float:
    # Calculate score based on rules (60% weightage)
    score = 0
    max_possible_score = 0
    
    # Skills matching with Jaccard similarity
    internship_skills = set(skill.strip().lower() for skill in internship.skill.description.split(',')) if internship.skill else set()
    student_skills = set(skill.strip().lower() for skill in student_data['skills'])
    
    if internship_skills and student_skills:
        intersection = len(internship_skills.intersection(student_skills))
        
        # Check partial matches
        partial_matches = 0
        for student_skill in student_skills:
            for internship_skill in internship_skills:
                if student_skill in internship_skill or internship_skill in student_skill:
                    partial_matches += 1
                    break
        
        exact_ratio = intersection / len(internship_skills) if internship_skills else 0
        partial_ratio = partial_matches / len(internship_skills) if internship_skills else 0
        
        skill_score = max(exact_ratio, partial_ratio * 0.7)
        score += skill_score * SKILL_MATCH_WEIGHT
    max_possible_score += SKILL_MATCH_WEIGHT
    
    # Sector matching
    if internship.sector and internship.sector.name.lower() == student_data['sector'].lower():
        score += SECTOR_MATCH_WEIGHT
    elif internship.sector and student_data['sector']:
        sector_keywords = {
            'technology': ['tech', 'software', 'development', 'programming', 'it'],
            'analytics': ['data', 'analysis', 'research', 'statistics'],
            'marketing': ['digital', 'social', 'content', 'advertising'],
            'finance': ['financial', 'banking', 'investment', 'accounting']
        }
        
        student_sector_lower = student_data['sector'].lower()
        internship_sector_lower = internship.sector.name.lower()
        
        for sector, keywords in sector_keywords.items():
            if sector in student_sector_lower or sector in internship_sector_lower:
                if any(keyword in student_sector_lower or keyword in internship_sector_lower for keyword in keywords):
                    score += SECTOR_MATCH_WEIGHT * 0.5
                    break
    max_possible_score += SECTOR_MATCH_WEIGHT
    
    # Location matching
    if internship.location and internship.location.description.lower() == student_data['preferred_location'].lower():
        score += LOCATION_MATCH_WEIGHT
    elif internship.location and internship.location.description.lower() == "remote":
        score += LOCATION_MATCH_WEIGHT * 0.8
    max_possible_score += LOCATION_MATCH_WEIGHT
    
    # Education matching
    student_edu_level = EDUCATION_HIERARCHY.get(student_data['education'], 3)
    required_edu_level = EDUCATION_HIERARCHY.get(internship.education.description if internship.education else "Bachelor's", 3)
    
    if student_edu_level >= required_edu_level:
        score += EDUCATION_MATCH_WEIGHT
    elif student_edu_level >= required_edu_level - 1:
        score += EDUCATION_MATCH_WEIGHT * 0.8
    else:
        score += EDUCATION_MATCH_WEIGHT * 0.3
    max_possible_score += EDUCATION_MATCH_WEIGHT
    
    # Perfect match bonus
    skill_intersection = len(internship_skills.intersection(student_skills))
    skill_match_ratio = skill_intersection / len(internship_skills) if internship_skills else 0
    
    # Give bonus for good matches
    if skill_match_ratio >= 0.5:
        bonus = 0
        if internship.sector and internship.sector.name.lower() == student_data['sector'].lower():
            bonus += PERFECT_MATCH_BONUS * 0.6
        
        if internship.location and internship.location.description.lower() == student_data['preferred_location'].lower():
            bonus += PERFECT_MATCH_BONUS * 0.4
        
        if skill_match_ratio >= 0.7:
            bonus += PERFECT_MATCH_BONUS * 0.2
            
        score += bonus
    max_possible_score += PERFECT_MATCH_BONUS
    
    # Normalize to 0-60
    normalized_score = (score / max_possible_score) * 60 if max_possible_score > 0 else 0
    return normalized_score

def calculate_description_similarity_mock(internship_desc: str, student_desc: str) -> float:
    # Description similarity with keyword matching (40% weightage)
    if not internship_desc or not student_desc:
        return 15
    
    internship_desc = internship_desc.lower()
    student_desc = student_desc.lower()
    
    stop_words = {
        'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'as', 'are', 'was', 'were', 
        'to', 'in', 'for', 'of', 'with', 'by', 'this', 'that', 'these', 'those', 'will',
        'have', 'has', 'had', 'do', 'does', 'did', 'can', 'could', 'would', 'should',
        'you', 'your', 'we', 'our', 'they', 'their', 'it', 'its', 'be', 'been', 'being'
    }
    
    internship_words = set(word for word in internship_desc.split() if word not in stop_words and len(word) > 2)
    student_words = set(word for word in student_desc.split() if word not in stop_words and len(word) > 2)
    
    # Domain-specific keywords
    tech_keywords = {'python', 'java', 'javascript', 'react', 'nodejs', 'sql', 'database', 'api', 'web', 'development', 'programming', 'software', 'coding', 'algorithm'}
    data_keywords = {'data', 'analysis', 'machine', 'learning', 'statistics', 'analytics', 'visualization', 'modeling', 'research', 'insights'}
    business_keywords = {'business', 'management', 'strategy', 'finance', 'marketing', 'sales', 'consulting', 'operations'}
    
    similarity_score = 0
    
    if internship_words and student_words:
        intersection = len(internship_words.intersection(student_words))
        union = len(internship_words.union(student_words))
        jaccard_similarity = intersection / union if union > 0 else 0
        similarity_score += jaccard_similarity * 20
        
        # Domain-specific matches bonus
        tech_matches = len(internship_words.intersection(student_words).intersection(tech_keywords))
        data_matches = len(internship_words.intersection(student_words).intersection(data_keywords))
        business_matches = len(internship_words.intersection(student_words).intersection(business_keywords))
        
        domain_bonus = (tech_matches + data_matches + business_matches) * 5
        similarity_score += min(domain_bonus, 15)
        
        # Partial keyword matching bonus
        partial_matches = 0
        for student_word in student_words:
            for internship_word in internship_words:
                if len(student_word) > 4 and len(internship_word) > 4:
                    if student_word in internship_word or internship_word in student_word:
                        partial_matches += 1
        
        similarity_score += min(partial_matches * 2, 10)
    
    if similarity_score < 15:
        similarity_score = 15
    
    return min(similarity_score, 40)

def calculate_total_score(internship: Internship, student_data: Dict) -> float:
    # Calculate total score combining rule-based (60%) and description similarity (40%)
    rule_score = calculate_rule_based_score(internship, student_data)

    ml_score = calculate_description_similarity_mock(
        internship.description, 
        student_data.get('description', '')
    )
    
    total_score = rule_score + ml_score

    return min(total_score, 100)
