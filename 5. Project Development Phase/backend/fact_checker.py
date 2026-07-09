"""
Fact Checker Service
Uses Wikipedia API to retrieve and summarize factual information about topics.
Provides quick fact verification for networking preparation.
"""

import logging
from typing import Optional, Dict, Any
import wikipediaapi

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FactChecker:
    """
    A service to verify facts and retrieve summaries using Wikipedia API.
    
    This class encapsulates all fact-checking functionality, providing
    reliable information sources for networking conversation preparation.
    """
    
    # def __init__(self, language: str = 'en'):
    #     """
    #     Initialize the FactChecker with Wikipedia API.
        
    #     Args:
    #         language (str): Language code for Wikipedia (default: 'en' for English)
    #     """
    #     self.wiki = wikipediaapi.Wikipedia(language=language)
    #     self.language = language
    #     logger.info(f"FactChecker initialized with language: {language}")
    def __init__(self, language: str = 'en'):
        """
        Initialize the FactChecker with Wikipedia API.
        
        Args:
            language (str): Language code for Wikipedia (default: 'en' for English)
        """
        # Wikipedia requires a descriptive user agent string to identify your application
        user_agent = "PersonalizedNetworkingAssistant/1.0 (student.project@annamacharya.edu)"
        
        self.wiki = wikipediaapi.Wikipedia(
            user_agent=user_agent,
            language=language
        )
        self.language = language
        logger.info(f"FactChecker initialized with language: {language}")
        

    def check_fact(self, query: str, max_summary_length: int = 300) -> Dict[str, Any]:
        """
        Search for a fact on Wikipedia and return a structured summary.
        
        Args:
            query (str): The topic or fact to search for
            max_summary_length (int): Maximum length of summary in characters (default: 300)
        
        Returns:
            Dict[str, Any]: A structured response containing:
                - 'found': bool indicating if the topic was found
                - 'title': The exact Wikipedia page title
                - 'summary': A concise summary of the topic
                - 'url': Direct link to the Wikipedia page
                - 'error': Error message if something went wrong (None if successful)
        
        Example:
            >>> checker = FactChecker()
            >>> result = checker.check_fact("blockchain in healthcare")
            >>> print(result['summary'])
        """
        
        try:
            # Log the incoming query
            logger.info(f"Searching for fact: '{query}'")
            
            # Normalize the query (strip whitespace)
            query = query.strip()
            
            if not query:
                logger.warning("Empty query provided to check_fact")
                return {
                    'found': False,
                    'title': None,
                    'summary': None,
                    'url': None,
                    'error': 'Query cannot be empty'
                }
            
            # Fetch the page from Wikipedia
            page = self.wiki.page(query)
            
            # Check if page exists and is valid
            if not page.exists():
                logger.warning(f"Page not found for query: '{query}'")
                return {
                    'found': False,
                    'title': query,
                    'summary': None,
                    'url': None,
                    'error': f"No Wikipedia page found for '{query}'"
                }
            
            # Extract summary and truncate if necessary
            full_summary = page.summary
            if len(full_summary) > max_summary_length:
                summary = full_summary[:max_summary_length] + "..."
            else:
                summary = full_summary
            
            # Construct the Wikipedia URL
            url = page.fullurl
            
            logger.info(f"Successfully retrieved fact: '{page.title}'")
            
            return {
                'found': True,
                'title': page.title,
                'summary': summary,
                'url': url,
                'error': None
            }
        
        except Exception as e:
            # Catch any unexpected errors
            logger.error(f"Error checking fact for query '{query}': {str(e)}")
            return {
                'found': False,
                'title': query,
                'summary': None,
                'url': None,
                'error': f"Error retrieving information: {str(e)}"
            }
    
    def check_multiple_facts(self, queries: list) -> list:
        """
        Check multiple facts in sequence.
        
        Args:
            queries (list): List of topic/fact strings to check
        
        Returns:
            list: List of result dictionaries from check_fact()
        
        Example:
            >>> checker = FactChecker()
            >>> results = checker.check_multiple_facts(
            ...     ["AI ethics", "sustainable computing", "blockchain"]
            ... )
        """
        logger.info(f"Checking {len(queries)} facts")
        results = []
        
        for query in queries:
            result = self.check_fact(query)
            results.append(result)
        
        logger.info(f"Completed checking {len(queries)} facts")
        return results
    
    def get_related_topics(self, query: str) -> Dict[str, Any]:
        """
        Retrieve a fact's summary along with links to related topics.
        
        Args:
            query (str): The main topic to search for
        
        Returns:
            Dict[str, Any]: Contains main fact result plus related links
        
        Example:
            >>> checker = FactChecker()
            >>> result = checker.get_related_topics("machine learning")
        """
        logger.info(f"Getting related topics for: '{query}'")
        
        main_fact = self.check_fact(query)
        
        try:
            page = self.wiki.page(query)
            
            if page.exists():
                # Extract links from the page (up to 10 related topics)
                related_links = list(page.links.keys())[:10]
                main_fact['related_topics'] = related_links
            else:
                main_fact['related_topics'] = []
        
        except Exception as e:
            logger.warning(f"Could not retrieve related topics: {str(e)}")
            main_fact['related_topics'] = []
        
        return main_fact


def create_fact_checker() -> FactChecker:
    """
    Factory function to create a FactChecker instance.
    
    Returns:
        FactChecker: A configured instance ready for use
    
    Example:
        >>> checker = create_fact_checker()
        >>> result = checker.check_fact("AI")
    """
    return FactChecker()
