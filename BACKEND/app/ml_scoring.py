# ML-Enhanced Scoring System combining rule-based (60%) and ML similarity (40%)
import os
import pickle
import time
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import re
from app.models import Internship
from app.scoring import calculate_rule_based_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.preprocessing import normalize
    import numpy as np
    import re
    ML_AVAILABLE = True
    logger.info("ML libraries loaded successfully")
except ImportError:
    logger.warning("ML libraries not available. Using rule-based scoring only.")
    ML_AVAILABLE = False

class HybridRecommendationEngine:
    # Hybrid recommendation engine with rule-based and ML approaches
    
    def __init__(self):
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.internship_texts = []
        self.internship_metadata = []  # Store additional metadata
        self.model_path = "ml_model.pkl"
        self.model_version = "2.0"
        self.last_training_time = None
        self.training_data_hash = None
        
        # Performance tracking
        self.similarity_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.performance_metrics = {}  # Add missing performance_metrics
        
        # Try to load existing model
        if ML_AVAILABLE:
            self._load_model()
    
    def _preprocess_text(self, text: str) -> str:
        """Enhanced text preprocessing for better feature extraction"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces and commas
        text = re.sub(r'[^\w\s,]', ' ', text)
        
        # Replace commas with spaces to separate skills properly
        text = text.replace(',', ' ')
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Enhanced technology-specific preprocessing
        tech_replacements = {
            'javascript': 'js',
            'typescript': 'ts',
            'machine learning': 'ml',
            'artificial intelligence': 'ai',
            'user interface': 'ui',
            'user experience': 'ux',
            'application programming interface': 'api',
            'database': 'db',
            'full stack': 'fullstack',
            'react native': 'reactnative',
            'node js': 'nodejs',
            'spring boot': 'springboot',
            'after effects': 'aftereffects',
            'premiere pro': 'premierepro',
            'adobe xd': 'adobexd',
            'computer vision': 'computervision',
            'natural language processing': 'nlp',
            'big data': 'bigdata',
            'quality assurance': 'qa',
            'business intelligence': 'bi',
            'penetration testing': 'pentest'
        }
        
        for old_term, new_term in tech_replacements.items():
            text = text.replace(old_term, new_term)
        
        return text

    def _load_model(self):
        """Load pre-trained ML model with version checking"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                # Check model version compatibility
                model_version = model_data.get('version', '1.0')
                if model_version != self.model_version:
                    logger.warning(f"Model version mismatch. Expected {self.model_version}, got {model_version}")
                    return
                
                self.tfidf_vectorizer = model_data['vectorizer']
                self.tfidf_matrix = model_data['tfidf_matrix']
                self.internship_texts = model_data['internship_texts']
                self.internship_metadata = model_data.get('internship_metadata', [])
                self.last_training_time = model_data.get('training_time')
                self.training_data_hash = model_data.get('data_hash')
                
                logger.info(f"Model v{model_version} loaded successfully (trained on {len(self.internship_texts)} internships)")
                if self.last_training_time:
                    logger.info(f"Last training: {self.last_training_time}")
            else:
                logger.info("No existing model found")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self._reset_model()
    
    def _reset_model(self):
        """Reset model state"""
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.internship_texts = []
        self.internship_metadata = []
        self.similarity_cache.clear()

    def _save_model(self):
        """Save trained ML model with metadata"""
        try:
            model_data = {
                'version': self.model_version,
                'vectorizer': self.tfidf_vectorizer,
                'tfidf_matrix': self.tfidf_matrix,
                'internship_texts': self.internship_texts,
                'internship_metadata': self.internship_metadata,
                'training_time': datetime.now().isoformat(),
                'data_hash': self.training_data_hash,
                'performance_metrics': self.performance_metrics
            }
            
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Model v{self.model_version} saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")

    def _extract_text_features(self, internship):
        """Enhanced text feature extraction with weighted importance"""
        text_features = []
        
        # Title/Role (highest importance - repeat 3x for emphasis)
        if hasattr(internship, 'title') and internship.title:
            title_text = self._preprocess_text(internship.title)
            text_features.extend([title_text] * 3)
        
        # Skills (high importance - repeat 2x)
        if hasattr(internship, 'skill') and internship.skill and internship.skill.description:
            skills_text = self._preprocess_text(internship.skill.description)
            text_features.extend([skills_text] * 2)
        
        # Sector (high importance - repeat 2x)
        if hasattr(internship, 'sector') and internship.sector:
            sector_text = self._preprocess_text(internship.sector.name)
            text_features.extend([sector_text] * 2)
        
        # Description (medium importance)
        if hasattr(internship, 'description') and internship.description:
            desc_text = self._preprocess_text(internship.description)
            text_features.append(desc_text)
        
        # Location (lower importance)
        if hasattr(internship, 'location') and internship.location:
            location_text = self._preprocess_text(internship.location.description)
            text_features.append(location_text)
        
        combined_text = ' '.join(filter(None, text_features))
        return combined_text if combined_text.strip() else "internship opportunity"
    
    def is_ready_for_ml(self) -> bool:
        """Check if ML model is ready for use"""
        return (ML_AVAILABLE and 
                self.tfidf_vectorizer is not None and 
                self.tfidf_matrix is not None and 
                len(self.internship_texts) > 0)
    
    def train_manually(self, internships: List[Internship], force_retrain: bool = False):
        """Enhanced training method with better preprocessing and caching"""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available for training")
            return False
        
        # Check if retraining is needed
        if not force_retrain and self.is_ready_for_ml():
            # Check if data has changed
            current_data_hash = self._calculate_data_hash(internships)
            if current_data_hash == self.training_data_hash:
                logger.info("Model already trained with current data")
                return True
        
        try:
            logger.info(f"Training ML model with {len(internships)} internships...")
            start_time = time.time()
            
            # Prepare enhanced text data for training
            self.internship_texts = []
            self.internship_metadata = []
            
            for idx, internship in enumerate(internships):
                # Extract enhanced text features
                combined_text = self._extract_text_features(internship)
                self.internship_texts.append(combined_text)
                
                # Store metadata for analysis
                metadata = {
                    'id': getattr(internship, 'id', idx),
                    'title': getattr(internship, 'title', ''),
                    'sector': getattr(internship, 'sector', ''),
                    'text_length': len(combined_text)
                }
                self.internship_metadata.append(metadata)
            
            # Enhanced TF-IDF vectorizer with better parameters
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=8000,  # Increased for better feature capture
                stop_words='english',
                ngram_range=(1, 3),  # Include trigrams for better context
                min_df=1,
                max_df=0.90,  # Slightly lower to include more distinctive terms
                sublinear_tf=True,  # Better handling of term frequency
                norm='l2',  # L2 normalization for cosine similarity
                lowercase=True,
                token_pattern=r'\b\w+\b'  # Include single letters (useful for tech terms)
            )
            
            # Fit and transform the text data
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.internship_texts)
            
            # Calculate and store training metadata
            training_time = time.time() - start_time
            self.training_data_hash = self._calculate_data_hash(internships)
            self.last_training_time = datetime.now()
            
            # Performance metrics
            self.performance_metrics = {
                'training_time': training_time,
                'vocabulary_size': len(self.tfidf_vectorizer.vocabulary_),
                'matrix_shape': self.tfidf_matrix.shape,
                'sparsity': 1.0 - (self.tfidf_matrix.nnz / (self.tfidf_matrix.shape[0] * self.tfidf_matrix.shape[1]))
            }
            
            # Save the enhanced model
            self._save_model()
            
            logger.info(f"ML training completed in {training_time:.2f}s")
            logger.info(f"Matrix shape: {self.tfidf_matrix.shape}")
            logger.info(f"Vocabulary size: {len(self.tfidf_vectorizer.vocabulary_)}")
            logger.info(f"Matrix sparsity: {self.performance_metrics['sparsity']:.3f}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            self._reset_model()
            return False
    
    def _calculate_data_hash(self, internships: List[Internship]) -> str:
        """Calculate hash of training data to detect changes"""
        try:
            data_string = ""
            for internship in internships:
                data_string += f"{getattr(internship, 'id', '')}:"
                data_string += f"{getattr(internship, 'title', '')}:"
                data_string += f"{getattr(internship, 'description', '')}:"
                data_string += f"{getattr(internship, 'sector', '')}"
            
            return hashlib.md5(data_string.encode()).hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate data hash: {e}")
            return str(time.time())
    
    def calculate_ml_similarity(self, student_profile: str, internship_idx: int) -> float:
        """Enhanced ML-based similarity calculation with caching"""
        if not self.is_ready_for_ml():
            return 25.0  # Neutral fallback score (out of 40)
        
        try:
            # Check cache first
            cache_key = hashlib.md5(f"{student_profile}_{internship_idx}".encode()).hexdigest()
            if cache_key in self.similarity_cache:
                return self.similarity_cache[cache_key]
            
            # Preprocess student profile
            processed_profile = self._preprocess_text(student_profile)
            
            # Transform student profile using trained vectorizer
            student_vector = self.tfidf_vectorizer.transform([processed_profile])
            
            # Ensure internship index is valid
            if internship_idx >= len(self.internship_texts):
                internship_idx = internship_idx % len(self.internship_texts)
            
            # Get internship vector
            internship_vector = self.tfidf_matrix[internship_idx]
            
            # Calculate cosine similarity
            similarity = cosine_similarity(student_vector, internship_vector)[0][0]
            
            # Enhanced scoring with multiple factors
            base_score = similarity * 40
            
            # Bonus for high-quality matches
            if similarity > 0.7:
                base_score *= 1.1  # 10% bonus for excellent matches
            elif similarity > 0.5:
                base_score *= 1.05  # 5% bonus for good matches
            
            # Ensure reasonable score range
            ml_score = max(min(base_score, 40.0), 15.0)  # Between 15-40
            
            # Cache the result
            self.similarity_cache[cache_key] = ml_score
            
            return ml_score
            
        except Exception as e:
            logger.error(f"Error in ML similarity calculation: {e}")
            return 25.0  # Fallback score


# Global instance
recommendation_engine = HybridRecommendationEngine()


def calculate_enhanced_score(internship: Internship, student_data: Dict, internship_idx: int = 0) -> Tuple[float, Dict]:
    """
    Enhanced scoring with detailed breakdown and diagnostics
    Returns: (total_score, score_breakdown)
    """
    try:
        # Rule-based score (60%)
        rule_score = calculate_rule_based_score(internship, student_data)
        
        # ML-based score (40%) - only if model is ready
        ml_details = {"status": "not_available", "score": 25}
        
        if recommendation_engine.is_ready_for_ml():
            # Build comprehensive student profile
            profile_parts = []
            
            if student_data.get('description'):
                profile_parts.append(student_data['description'])
            
            if student_data.get('skills'):
                skills_text = ' '.join(student_data['skills'])
                profile_parts.append(skills_text)
            
            if student_data.get('sector'):
                profile_parts.append(student_data['sector'])
            
            if student_data.get('education'):
                profile_parts.append(student_data['education'])
            
            student_profile = ' '.join(profile_parts)
            
            if student_profile.strip():
                ml_score = recommendation_engine.calculate_ml_similarity(student_profile, internship_idx)
                ml_details = {
                    "status": "calculated",
                    "score": ml_score,
                    "profile_length": len(student_profile)
                }
            else:
                ml_score = 25  # Neutral score for empty profile
                ml_details = {"status": "empty_profile", "score": ml_score}
        else:
            ml_score = 25  # Neutral fallback
            ml_details = {"status": "model_not_ready", "score": ml_score}
        
        # Ensure ML score helps (minimum 50% of max)
        ml_score = max(ml_score, 20)
        ml_details["final_score"] = ml_score
        
        # Calculate total with safeguards
        total_score = min(rule_score + ml_score, 100)
        
        # Detailed breakdown for debugging/analysis
        score_breakdown = {
            "total_score": total_score,
            "rule_based": {
                "score": rule_score,
                "weight": 0.6
            },
            "ml_based": {
                **ml_details,
                "weight": 0.4
            },
            "internship_idx": internship_idx,
            "internship_id": getattr(internship, 'id', None)
        }
        
        return total_score, score_breakdown
        
    except Exception as e:
        logger.error(f"Error in enhanced scoring: {e}")
        # Fallback to rule-based only
        fallback_score = calculate_rule_based_score(internship, student_data) + 25
        return min(fallback_score, 100), {"error": str(e), "fallback": True}


def get_model_status() -> Dict:
    """Get comprehensive ML model status and performance metrics"""
    status = {
        "ml_available": ML_AVAILABLE,
        "is_trained": recommendation_engine.is_ready_for_ml(),
        "training_size": len(recommendation_engine.internship_texts) if recommendation_engine.internship_texts else 0,
        "model_file_exists": os.path.exists(recommendation_engine.model_path),
        "model_version": recommendation_engine.model_version,
        "cache_size": len(recommendation_engine.similarity_cache)
    }
    
    # Add performance metrics if available
    if recommendation_engine.performance_metrics:
        status["performance_metrics"] = recommendation_engine.performance_metrics
    
    # Add training information if available
    if recommendation_engine.last_training_time:
        status["last_training"] = recommendation_engine.last_training_time.isoformat()
    
    # Add vocabulary info if model is trained
    if recommendation_engine.tfidf_vectorizer:
        status["vocabulary_size"] = len(recommendation_engine.tfidf_vectorizer.vocabulary_)
    
    return status


def clear_model_cache():
    """Clear similarity cache to free memory"""
    recommendation_engine.similarity_cache.clear()
    logger.info("Model cache cleared")


def retrain_model_if_needed(internships: List[Internship]) -> bool:
    """Check if model needs retraining and retrain if necessary"""
    try:
        current_hash = recommendation_engine._calculate_data_hash(internships)
        
        if (not recommendation_engine.is_ready_for_ml() or 
            current_hash != recommendation_engine.training_data_hash):
            
            logger.info("Data changed, retraining model...")
            return recommendation_engine.train_manually(internships, force_retrain=True)
        
        logger.info("Model is up to date")
        return True
        
    except Exception as e:
        logger.error(f"Error checking model status: {e}")
        return False
