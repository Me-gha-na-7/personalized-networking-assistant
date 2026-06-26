"""
Event Analyzer Service
Uses DistilBERT with zero-shot classification to extract relevant themes
and topics from event descriptions.
"""

import logging
from typing import List, Dict, Any, Tuple
from transformers import pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EventAnalyzer:
    """
    A service to analyze event descriptions and extract relevant themes
    using zero-shot classification with DistilBERT.
    
    This class uses natural language understanding to identify key topics
    and themes from event descriptions, helping users prepare relevant
    conversation starters aligned with event focus.
    """
    
    # Default candidate themes for zero-shot classification
    DEFAULT_CANDIDATE_LABELS = [
        "artificial intelligence",
        "sustainability",
        "climate change",
        "urban planning",
        "healthcare",
        "blockchain",
        "cybersecurity",
        "data science",
        "machine learning",
        "cloud computing",
        "renewable energy",
        "fintech",
        "agriculture",
        "education technology",
        "innovation",
        "entrepreneurship",
        "leadership",
        "business strategy",
        "marketing",
        "social impact"
    ]
    
    # def __init__(
    #     self,
    #     model_name: str = "distilbert-base-uncased-mnli",
    #     candidate_labels: List[str] = None
    # ):
    #     """
    #     Initialize the EventAnalyzer with DistilBERT model.
        
    #     Args:
    #         model_name (str): HuggingFace model identifier (default: distilbert-base-uncased-mnli)
    #         candidate_labels (List[str]): List of potential themes to classify against.
    #                                      If None, uses DEFAULT_CANDIDATE_LABELS
        
    #     Raises:
    #         Exception: If model cannot be loaded
        
    #     Example:
    #         >>> analyzer = EventAnalyzer()
    #         >>> analyzer.analyze_event("AI for Sustainable Cities")
    #     """
    #     try:
    #         logger.info(f"Loading model: {model_name}")
            
    #         # Initialize the zero-shot classification pipeline
    #         self.classifier = pipeline(
    #             "zero-shot-classification",
    #             model=model_name,
    #             device=-1  # Use CPU; change to 0 for GPU
    #         )
            
    #         # Set candidate labels
    #         self.candidate_labels = candidate_labels or self.DEFAULT_CANDIDATE_LABELS
            
    #         logger.info(f"EventAnalyzer initialized successfully with {len(self.candidate_labels)} candidate labels")
        
    #     except Exception as e:
    #         logger.error(f"Failed to initialize EventAnalyzer: {str(e)}")
    #         raise Exception(f"Could not load model '{model_name}': {str(e)}")
    def __init__(
        self,
        model_name: str = "typeform/distilbert-base-uncased-mnli",
        candidate_labels: List[str] = None
    ):
        """
        Initialize the EventAnalyzer with DistilBERT model.
        
        Args:
            model_name (str): HuggingFace model identifier (default: typeform/distilbert-base-uncased-mnli)
            candidate_labels (List[str]): List of potential themes to classify against.
                                         If None, uses DEFAULT_CANDIDATE_LABELS
        
        Raises:
            Exception: If model cannot be loaded
        
        Example:
            >>> analyzer = EventAnalyzer()
            >>> analyzer.analyze_event("AI for Sustainable Cities")
        """
        try:
            logger.info(f"Loading model: {model_name}")
            
            # Initialize the zero-shot classification pipeline
            self.classifier = pipeline(
                "zero-shot-classification",
                model=model_name,
                device=-1  # Use CPU; change to 0 for GPU
            )
            
            # Set candidate labels
            self.candidate_labels = candidate_labels or self.DEFAULT_CANDIDATE_LABELS
            
            logger.info(f"EventAnalyzer initialized successfully with {len(self.candidate_labels)} candidate labels")
        
        except Exception as e:
            logger.error(f"Failed to initialize EventAnalyzer: {str(e)}")
            raise Exception(f"Could not load model '{model_name}': {str(e)}")
        
    def analyze_event(
        self,
        event_description: str,
        top_k: int = 3,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """
        Analyze an event description and extract the top themes.
        
        Args:
            event_description (str): The event description to analyze
            top_k (int): Number of top themes to return (default: 3)
            threshold (float): Confidence threshold for themes (0-1, default: 0.1)
        
        Returns:
            Dict[str, Any]: Contains:
                - 'event_description': The original input
                - 'extracted_themes': List of theme dicts with 'label' and 'score'
                - 'primary_theme': The top-ranked theme
                - 'error': None if successful, error message otherwise
        
        Example:
            >>> analyzer = EventAnalyzer()
            >>> result = analyzer.analyze_event(
            ...     "AI for Sustainable Cities",
            ...     top_k=3
            ... )
            >>> print(result['primary_theme'])
        """
        
        try:
            # Validate input
            if not event_description or not event_description.strip():
                logger.warning("Empty event description provided")
                return {
                    'event_description': event_description,
                    'extracted_themes': [],
                    'primary_theme': None,
                    'error': 'Event description cannot be empty'
                }
            
            event_description = event_description.strip()
            logger.info(f"Analyzing event: '{event_description[:50]}...'")
            
            # Perform zero-shot classification
            result = self.classifier(
                event_description,
                self.candidate_labels,
                multi_class=True  # Allow multiple labels per example
            )
            
            # Extract and filter themes by score
            extracted_themes = []
            for label, score in zip(result['labels'], result['scores']):
                if score >= threshold:
                    extracted_themes.append({
                        'label': label,
                        'score': round(score, 4)
                    })
            
            # Keep only top_k themes
            extracted_themes = extracted_themes[:top_k]
            
            # Determine primary theme
            primary_theme = extracted_themes[0]['label'] if extracted_themes else None
            
            logger.info(f"Extracted {len(extracted_themes)} themes; primary: '{primary_theme}'")
            
            return {
                'event_description': event_description,
                'extracted_themes': extracted_themes,
                'primary_theme': primary_theme,
                'error': None
            }
        
        except Exception as e:
            logger.error(f"Error analyzing event: {str(e)}")
            return {
                'event_description': event_description,
                'extracted_themes': [],
                'primary_theme': None,
                'error': f"Failed to analyze event: {str(e)}"
            }
    
    def analyze_with_custom_labels(
        self,
        event_description: str,
        custom_labels: List[str],
        top_k: int = 3,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """
        Analyze an event using custom candidate labels instead of defaults.
        
        Args:
            event_description (str): The event description to analyze
            custom_labels (List[str]): Custom list of themes to classify against
            top_k (int): Number of top themes to return
            threshold (float): Confidence threshold for themes
        
        Returns:
            Dict[str, Any]: Same structure as analyze_event()
        
        Example:
            >>> analyzer = EventAnalyzer()
            >>> result = analyzer.analyze_with_custom_labels(
            ...     "AI for Sustainable Cities",
            ...     ["AI", "climate", "sustainability", "policy"],
            ...     top_k=2
            ... )
        """
        logger.info(f"Analyzing with {len(custom_labels)} custom labels")
        
        try:
            if not custom_labels or len(custom_labels) == 0:
                raise ValueError("Custom labels list cannot be empty")
            
            if not event_description or not event_description.strip():
                logger.warning("Empty event description provided")
                return {
                    'event_description': event_description,
                    'extracted_themes': [],
                    'primary_theme': None,
                    'error': 'Event description cannot be empty'
                }
            
            event_description = event_description.strip()
            logger.info(f"Analyzing event with custom labels: '{event_description[:50]}...'")
            
            # Perform classification with custom labels
            result = self.classifier(
                event_description,
                custom_labels,
                multi_class=True
            )
            
            # Extract and filter themes
            extracted_themes = []
            for label, score in zip(result['labels'], result['scores']):
                if score >= threshold:
                    extracted_themes.append({
                        'label': label,
                        'score': round(score, 4)
                    })
            
            extracted_themes = extracted_themes[:top_k]
            primary_theme = extracted_themes[0]['label'] if extracted_themes else None
            
            logger.info(f"Extracted {len(extracted_themes)} themes with custom labels")
            
            return {
                'event_description': event_description,
                'extracted_themes': extracted_themes,
                'primary_theme': primary_theme,
                'error': None
            }
        
        except Exception as e:
            logger.error(f"Error analyzing with custom labels: {str(e)}")
            return {
                'event_description': event_description,
                'extracted_themes': [],
                'primary_theme': None,
                'error': f"Failed to analyze with custom labels: {str(e)}"
            }
    
    def compare_event_themes(
        self,
        event_description: str,
        user_interests: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze event themes and compare with user interests for alignment.
        
        Args:
            event_description (str): The event description
            user_interests (List[str]): List of user's interests/skills
        
        Returns:
            Dict[str, Any]: Contains:
                - 'event_description': Original event description
                - 'extracted_themes': Themes from event
                - 'user_interests': User's provided interests
                - 'alignment_score': 0-1 score indicating theme-interest overlap
                - 'matching_interests': Interests that match with event themes
                - 'error': None if successful
        
        Example:
            >>> analyzer = EventAnalyzer()
            >>> result = analyzer.compare_event_themes(
            ...     "AI for Sustainable Cities",
            ...     ["machine learning", "climate change", "urban policy"]
            ... )
            >>> print(result['alignment_score'])
        """
        
        try:
            logger.info("Comparing event themes with user interests")
            
            # First analyze the event
            event_analysis = self.analyze_event(event_description)
            
            if event_analysis['error']:
                return {
                    'event_description': event_description,
                    'extracted_themes': [],
                    'user_interests': user_interests,
                    'alignment_score': 0.0,
                    'matching_interests': [],
                    'error': event_analysis['error']
                }
            
            # Extract theme labels
            event_themes = [theme['label'].lower() for theme in event_analysis['extracted_themes']]
            
            # Normalize user interests
            normalized_interests = [interest.lower() for interest in user_interests]
            
            # Find matching interests
            matching_interests = [
                interest for interest in normalized_interests
                if any(interest in theme or theme in interest for theme in event_themes)
            ]
            
            # Calculate alignment score (0-1)
            if len(normalized_interests) == 0:
                alignment_score = 0.0
            else:
                alignment_score = round(len(matching_interests) / len(normalized_interests), 2)
            
            logger.info(f"Alignment score: {alignment_score} ({len(matching_interests)} matches)")
            
            return {
                'event_description': event_description,
                'extracted_themes': event_analysis['extracted_themes'],
                'user_interests': user_interests,
                'alignment_score': alignment_score,
                'matching_interests': matching_interests,
                'error': None
            }
        
        except Exception as e:
            logger.error(f"Error comparing themes with interests: {str(e)}")
            return {
                'event_description': event_description,
                'extracted_themes': [],
                'user_interests': user_interests,
                'alignment_score': 0.0,
                'matching_interests': [],
                'error': f"Failed to compare themes: {str(e)}"
            }
    
    def get_candidate_labels(self) -> List[str]:
        """
        Get the current list of candidate labels used for classification.
        
        Returns:
            List[str]: List of candidate theme labels
        """
        return self.candidate_labels
    
    def set_candidate_labels(self, new_labels: List[str]) -> None:
        """
        Update the candidate labels for classification.
        
        Args:
            new_labels (List[str]): New list of candidate labels
        """
        if not new_labels or len(new_labels) == 0:
            logger.warning("Attempted to set empty candidate labels")
            return
        
        self.candidate_labels = new_labels
        logger.info(f"Updated candidate labels to {len(new_labels)} labels")


def create_event_analyzer(
    model_name: str = "typeform/distilbert-base-uncased-mnli",
    custom_labels: List[str] = None
) -> EventAnalyzer:
    """
    Factory function to create an EventAnalyzer instance.
    
    Args:
        model_name (str): HuggingFace model identifier
        custom_labels (List[str]): Optional custom candidate labels
    
    Returns:
        EventAnalyzer: A configured instance ready for use
    
    Example:
        >>> analyzer = create_event_analyzer()
        >>> result = analyzer.analyze_event("Startup pitch event")
    """
    return EventAnalyzer(model_name=model_name, candidate_labels=custom_labels)
