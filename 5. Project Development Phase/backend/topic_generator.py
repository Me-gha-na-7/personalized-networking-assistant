"""
Topic Generator Service
Uses GPT-2 text-generation pipeline to create natural, context-aware
conversation starters for networking events based on extracted themes
and user interests.
"""

import logging
import re
from typing import List, Dict, Any
from transformers import pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TopicGenerator:
    """
    A service to generate natural conversation starters for networking events
    using GPT-2 text generation.
    
    This class creates context-aware, engaging conversation prompts based on
    event themes and user interests, helping users initiate meaningful
    conversations at professional and social networking events.
    """
    
    def __init__(self, model_name: str = "gpt2"):
        """
        Initialize the TopicGenerator with GPT-2 model.
        
        Args:
            model_name (str): HuggingFace model identifier (default: "gpt2")
        
        Raises:
            Exception: If model cannot be loaded
        
        Example:
            >>> generator = TopicGenerator()
            >>> starters = generator.generate_starters(
            ...     themes=["AI", "sustainability"],
            ...     interests=["climate change", "innovation"]
            ... )
        """
        try:
            logger.info(f"Loading model: {model_name}")
            
            # Initialize the text-generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=model_name,
                device=-1,  # Use CPU; change to 0 for GPU
                max_length=100
            )
            
            logger.info("TopicGenerator initialized successfully")
        
        except Exception as e:
            logger.error(f"Failed to initialize TopicGenerator: {str(e)}")
            raise Exception(f"Could not load model '{model_name}': {str(e)}")
    
    def _create_prompt(
        self,
        themes: List[str],
        interests: List[str]
    ) -> str:
        """
        Create a carefully engineered prompt for GPT-2 based on themes and interests.
        
        Args:
            themes (List[str]): Extracted event themes
            interests (List[str]): User interests
        
        Returns:
            str: A prompt string to feed to GPT-2
        
        Example:
            >>> generator = TopicGenerator()
            >>> prompt = generator._create_prompt(
            ...     ["AI", "sustainability"],
            ...     ["climate change"]
            ... )
        """
        # Combine themes and interests for context
        combined = themes + interests
        combined_str = ", ".join(combined[:3])  # Use up to 3 items
        
        # Craft a prompt that guides GPT-2 to generate conversation starters
        prompt = (
            f"At a networking event focused on {combined_str}, "
            f"an engaging conversation starter would be: "
        )
        
        logger.debug(f"Created prompt: {prompt}")
        return prompt
    
    def _clean_generated_text(
        self,
        generated_text: str,
        prompt: str
    ) -> str:
        """
        Clean and extract the meaningful part of generated text.
        
        Removes the prompt prefix and cleans up artifacts from text generation.
        
        Args:
            generated_text (str): Raw output from GPT-2
            prompt (str): The prompt that was used
        
        Returns:
            str: Cleaned, natural conversation starter
        """
        # Remove the prompt from the output
        text = generated_text.replace(prompt, "").strip()
        
        # Remove incomplete sentences (those ending with partial words)
        sentences = text.split(". ")
        if len(sentences) > 0 and not sentences[-1].endswith(("?", ".", "!")):
            sentences = sentences[:-1]
        
        text = ". ".join(sentences)
        
        # Ensure text ends with proper punctuation
        if text and text[-1] not in (".", "?", "!"):
            if "?" in text and text.rfind("?") > text.rfind("."):
                text = text[:text.rfind("?") + 1]
            else:
                text = text + "."
        
        # Remove common artifacts and incomplete phrases
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()
        
        logger.debug(f"Cleaned text: {text}")
        return text
    
    def generate_starters(
        self,
        themes: List[str],
        interests: List[str],
        num_starters: int = 3,
        max_length: int = 100
    ) -> Dict[str, Any]:
        """
        Generate conversation starters based on event themes and user interests.
        
        Args:
            themes (List[str]): Extracted themes from event (e.g., ["AI", "sustainability"])
            interests (List[str]): User's interests (e.g., ["climate change", "innovation"])
            num_starters (int): Number of conversation starters to generate (default: 3)
            max_length (int): Maximum length of each generated starter in characters
        
        Returns:
            Dict[str, Any]: Contains:
                - 'themes': Input themes
                - 'interests': Input interests
                - 'conversation_starters': List of generated conversation strings
                - 'num_generated': Actual number of starters generated
                - 'error': None if successful, error message otherwise
        
        Example:
            >>> generator = TopicGenerator()
            >>> result = generator.generate_starters(
            ...     themes=["AI", "healthcare"],
            ...     interests=["data science", "digital transformation"],
            ...     num_starters=3
            ... )
            >>> for starter in result['conversation_starters']:
            ...     print(f"• {starter}")
        """
        
        try:
            # Validate inputs
            if not themes or len(themes) == 0:
                logger.warning("No themes provided to generate_starters")
                return {
                    'themes': themes,
                    'interests': interests,
                    'conversation_starters': [],
                    'num_generated': 0,
                    'error': 'At least one theme is required'
                }
            
            if not interests or len(interests) == 0:
                logger.warning("No interests provided to generate_starters")
                return {
                    'themes': themes,
                    'interests': interests,
                    'conversation_starters': [],
                    'num_generated': 0,
                    'error': 'At least one interest is required'
                }
            
            # Limit num_starters to reasonable range
            num_starters = max(1, min(num_starters, 5))
            
            logger.info(
                f"Generating {num_starters} conversation starters "
                f"for themes: {themes}, interests: {interests}"
            )
            
            conversation_starters = []
            
            # Generate multiple starters to ensure quality
            for i in range(num_starters):
                # Create a unique prompt for each generation
                prompt = self._create_prompt(themes, interests)
                
                try:
                    # Generate text using GPT-2
                    generated = self.generator(
                        prompt,
                        max_length=max_length,
                        num_return_sequences=1,
                        temperature=0.7,  # Add some randomness but keep coherence
                        do_sample=True,
                        top_k=50,
                        top_p=0.95
                    )
                    
                    # Extract the generated text
                    raw_text = generated[0]['generated_text']
                    
                    # Clean and format the text
                    clean_text = self._clean_generated_text(raw_text, prompt)
                    
                    # Ensure non-empty and unique starters
                    if clean_text and len(clean_text) > 10 and clean_text not in conversation_starters:
                        conversation_starters.append(clean_text)
                        logger.debug(f"Generated starter {i+1}: {clean_text}")
                
                except Exception as e:
                    logger.warning(f"Error generating starter {i+1}: {str(e)}")
                    continue
            
            # If we didn't generate enough starters, use fallback
            if len(conversation_starters) == 0:
                conversation_starters = self._generate_fallback_starters(themes, interests)
                logger.warning("Using fallback starters due to generation issues")
            
            logger.info(f"Successfully generated {len(conversation_starters)} conversation starters")
            
            return {
                'themes': themes,
                'interests': interests,
                'conversation_starters': conversation_starters,
                'num_generated': len(conversation_starters),
                'error': None
            }
        
        except Exception as e:
            logger.error(f"Error generating conversation starters: {str(e)}")
            return {
                'themes': themes,
                'interests': interests,
                'conversation_starters': self._generate_fallback_starters(themes, interests),
                'num_generated': 0,
                'error': f"Generation error: {str(e)}"
            }
    
    def _generate_fallback_starters(
        self,
        themes: List[str],
        interests: List[str]
    ) -> List[str]:
        """
        Generate fallback conversation starters if GPT-2 generation fails.
        
        Provides template-based starters to ensure the system always returns
        useful conversation prompts.
        
        Args:
            themes (List[str]): Event themes
            interests (List[str]): User interests
        
        Returns:
            List[str]: List of template-based conversation starters
        """
        logger.info("Generating fallback conversation starters")
        
        templates = [
            f"What drew you to this event focusing on {themes[0]}?",
            f"I'm particularly interested in {interests[0]}—have you explored this angle?",
            f"How do you see {themes[0]} evolving in relation to {interests[0]}?",
            f"What's your take on the intersection of {themes[0]} and {interests[0]}?",
            f"I'd love to hear about your experience with {themes[0] if themes else 'this topic'}.",
            f"Are you working on any {themes[0] if themes else 'innovative'} projects right now?",
            f"What's the most exciting development you've seen in {themes[0] if themes else 'this field'}?"
        ]
        
        # Select appropriate templates based on available themes and interests
        selected_starters = []
        for template in templates:
            if len(selected_starters) < 3:
                selected_starters.append(template)
        
        return selected_starters
    
    def generate_starters_with_follow_ups(
        self,
        themes: List[str],
        interests: List[str],
        num_starters: int = 2
    ) -> Dict[str, Any]:
        """
        Generate conversation starters with follow-up questions.
        
        Args:
            themes (List[str]): Event themes
            interests (List[str]): User interests
            num_starters (int): Number of starter/follow-up pairs (default: 2)
        
        Returns:
            Dict[str, Any]: Contains:
                - 'conversation_sets': List of dicts with 'starter' and 'follow_up'
                - 'error': Error message if any
        
        Example:
            >>> generator = TopicGenerator()
            >>> result = generator.generate_starters_with_follow_ups(
            ...     themes=["blockchain"],
            ...     interests=["fintech", "enterprise solutions"]
            ... )
            >>> for conv_set in result['conversation_sets']:
            ...     print(f"Opener: {conv_set['starter']}")
            ...     print(f"Follow-up: {conv_set['follow_up']}")
        """
        
        try:
            logger.info("Generating conversation starters with follow-ups")
            
            # First generate the main starters
            main_starters = self.generate_starters(themes, interests, num_starters)
            
            if main_starters['error']:
                return {
                    'conversation_sets': [],
                    'error': main_starters['error']
                }
            
            conversation_sets = []
            
            for starter in main_starters['conversation_starters']:
                # Generate follow-up based on the starter
                follow_up_prompt = f"After saying '{starter}', a natural follow-up would be: "
                
                try:
                    generated = self.generator(
                        follow_up_prompt,
                        max_length=80,
                        num_return_sequences=1,
                        temperature=0.6,
                        do_sample=True
                    )
                    
                    follow_up = self._clean_generated_text(
                        generated[0]['generated_text'],
                        follow_up_prompt
                    )
                
                except:
                    # Fallback follow-up
                    follow_up = f"Tell me more about your experience with {themes[0] if themes else 'that'}."
                
                conversation_sets.append({
                    'starter': starter,
                    'follow_up': follow_up
                })
            
            logger.info(f"Generated {len(conversation_sets)} conversation sets with follow-ups")
            
            return {
                'conversation_sets': conversation_sets,
                'error': None
            }
        
        except Exception as e:
            logger.error(f"Error generating follow-ups: {str(e)}")
            return {
                'conversation_sets': [],
                'error': f"Failed to generate follow-ups: {str(e)}"
            }


def create_topic_generator(model_name: str = "gpt2") -> TopicGenerator:
    """
    Factory function to create a TopicGenerator instance.
    
    Args:
        model_name (str): HuggingFace model identifier (default: "gpt2")
    
    Returns:
        TopicGenerator: A configured instance ready for use
    
    Example:
        >>> generator = create_topic_generator()
        >>> result = generator.generate_starters(
        ...     themes=["AI"],
        ...     interests=["machine learning", "ethics"]
        ... )
    """
    return TopicGenerator(model_name=model_name)
