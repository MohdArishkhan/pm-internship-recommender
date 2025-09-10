from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, crud

router = APIRouter()

@router.post("/", response_model=List[schemas.RecommendationResponse])
def get_recommendations(
    student_form: schemas.StudentForm,
    db: Session = Depends(get_db),
    use_ml: bool = Query(True, description="Use ML-enhanced scoring (default: True)")
):
    # Get recommendations using hybrid (ML + rules) or pure rule-based approach
    recommendations = crud.get_recommendations(db, student_form, use_ml=use_ml)
    
    if not recommendations:
        raise HTTPException(
            status_code=404, 
            detail="No matching internships found for your profile"
        )
    
    return recommendations


@router.post("/compare", response_model=dict)
def compare_approaches(
    student_form: schemas.StudentForm,
    db: Session = Depends(get_db)
):
    # Compare ML-enhanced vs rule-based recommendations
    ml_recommendations = crud.get_recommendations(db, student_form, use_ml=True)
    rule_recommendations = crud.get_recommendations(db, student_form, use_ml=False)
    
    return {
        "ml_enhanced": ml_recommendations[:5],
        "rule_based": rule_recommendations[:5],
        "summary": {
            "ml_avg_score": sum(r["match_score"] for r in ml_recommendations[:5]) / 5 if ml_recommendations else 0,
            "rule_avg_score": sum(r["match_score"] for r in rule_recommendations[:5]) / 5 if rule_recommendations else 0
        }
    }


@router.get("/model-status")
def get_model_status():
    # Get current ML model training status
    from app.ml_scoring import get_model_status
    return get_model_status()


@router.post("/retrain-model")
def retrain_model(
    force: bool = Query(False, description="Force retrain even if not needed"),
    db: Session = Depends(get_db)
):
    # Manually retrain the ML model
    from app.ml_scoring import recommendation_engine, ML_AVAILABLE
    from app import models
    
    if not ML_AVAILABLE:
        raise HTTPException(status_code=400, detail="ML libraries not available")
    
    internships = db.query(models.Internship).all()
    
    try:
        success = recommendation_engine.train_manually(internships, force_retrain=force)
        message = f"Model retrained successfully with {len(internships)} internships" if success else "Training failed"
    except Exception as e:
        success = False
        message = f"Training failed: {str(e)}"
    
    return {
        "success": success,
        "message": message,
        "training_size": len(internships),
        "is_trained": recommendation_engine.is_ready_for_ml()
    }


@router.post("/clear-cache")
def clear_model_cache():
    # Clear ML model cache to free memory
    from app.ml_scoring import clear_model_cache
    clear_model_cache()
    return {"message": "Model cache cleared successfully"}


@router.get("/detailed-score/{internship_id}")
def get_detailed_score(
    internship_id: int,
    student_form: schemas.StudentForm,
    db: Session = Depends(get_db)
):
    # Get detailed scoring breakdown for specific internship
    from app.ml_scoring import calculate_enhanced_score, ML_AVAILABLE
    from app import models
    
    internship = db.query(models.Internship).filter(models.Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    
    student_data = {
        'skills': student_form.skills,
        'education': student_form.education,
        'sector': student_form.sector,
        'location': student_form.location,
        'description': getattr(student_form, 'description', '')
    }
    
    if ML_AVAILABLE:
        score, breakdown = calculate_enhanced_score(internship, student_data, 0)
        return {
            "internship_id": internship_id,
            "internship_title": internship.title,
            "total_score": round(score, 2),
            "detailed_breakdown": breakdown
        }
    else:
        from app.crud import calculate_total_score
        score = calculate_total_score(internship, student_data)
        return {
            "internship_id": internship_id,
            "internship_title": internship.title,
            "total_score": round(score, 2),
            "method": "rule_based_only",
            "ml_available": False
        }
