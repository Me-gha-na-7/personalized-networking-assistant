"""
Personalized Networking Assistant - Streamlit Frontend
A professional, interactive web dashboard for generating smart conversation starters
for networking events, powered by AI and integrated with FastAPI backend.
"""

import streamlit as st
import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin

# ==================== CONFIGURATION ====================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Backend configuration
BACKEND_URL = "http://localhost:8000"
API_TIMEOUT = 30  # seconds

# Streamlit page configuration
st.set_page_config(
    page_title="Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding-top: 0rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Conversation starter card */
    .starter-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .starter-number {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .starter-text {
        font-size: 1.1rem;
        color: #333;
        font-style: italic;
        margin: 0.5rem 0;
    }
    
    /* Theme badge */
    .theme-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Success/Error messages */
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    
    .error-message {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    
    .info-message {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    
    /* History card */
    .history-card {
        background: #f9f9f9;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }
    
    .history-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .history-meta {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 1rem;
    }
    
    /* Fact check result */
    .fact-result {
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #00897b;
        margin-bottom: 1rem;
    }
    
    .fact-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #00695c;
        margin-bottom: 0.5rem;
    }
    
    .fact-summary {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .fact-link {
        display: inline-block;
        margin-top: 0.5rem;
        color: #00897b;
        text-decoration: none;
        font-weight: 500;
    }
    
    /* Button styling */
    .custom-button {
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        font-weight: 600;
    }
    
    /* Feedback buttons */
    .feedback-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .feedback-btn {
        flex: 1;
        padding: 0.5rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .thumbs-up {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .thumbs-down {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'event_description' not in st.session_state:
        st.session_state.event_description = ""
    if 'user_interests' not in st.session_state:
        st.session_state.user_interests = ""
    if 'generated_starters' not in st.session_state:
        st.session_state.generated_starters = None
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = None
    if 'fact_query' not in st.session_state:
        st.session_state.fact_query = ""
    if 'fact_result' not in st.session_state:
        st.session_state.fact_result = None
    if 'history_data' not in st.session_state:
        st.session_state.history_data = None
    if 'loading_history' not in st.session_state:
        st.session_state.loading_history = False
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = {}
    if 'api_error' not in st.session_state:
        st.session_state.api_error = None
    if 'api_success' not in st.session_state:
        st.session_state.api_success = None


initialize_session_state()

# ==================== API COMMUNICATION ====================

class NetworkingAssistantAPI:
    """Client for communicating with the FastAPI backend."""
    
    def __init__(self, base_url: str = BACKEND_URL, timeout: int = API_TIMEOUT):
        """
        Initialize API client.
        
        Args:
            base_url (str): Base URL of the FastAPI backend
            timeout (int): Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        logger.info(f"API client initialized with base URL: {base_url}")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None
    ) -> tuple[bool, Any, Optional[str]]:
        """
        Make HTTP request to backend with error handling.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint path
            data (Dict): Request payload for POST requests
        
        Returns:
            tuple: (success, data, error_message)
        """
        try:
            url = urljoin(self.base_url, endpoint)
            
            if method == "GET":
                response = requests.get(url, timeout=self.timeout)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=self.timeout)
            else:
                return False, None, f"Unsupported HTTP method: {method}"
            
            # Check if response is successful
            if response.status_code == 200:
                logger.info(f"✓ {method} {endpoint} - Status: {response.status_code}")
                return True, response.json(), None
            else:
                error_msg = f"Server error: {response.status_code}"
                try:
                    error_detail = response.json().get('detail', error_msg)
                    error_msg = error_detail
                except:
                    pass
                logger.error(f"✗ {method} {endpoint} - Status: {response.status_code}")
                return False, None, error_msg
        
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout (>{self.timeout}s). Is the backend running?"
            logger.error(f"Timeout error: {error_msg}")
            return False, None, error_msg
        except requests.exceptions.ConnectionError:
            error_msg = "Cannot connect to backend. Is it running on localhost:8000?"
            logger.error(f"Connection error: {error_msg}")
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Request error: {str(e)}"
            logger.error(f"Unexpected error: {error_msg}")
            return False, None, error_msg
    
    def health_check(self) -> tuple[bool, Optional[str]]:
        """
        Check if backend is healthy.
        
        Returns:
            tuple: (is_healthy, error_message)
        """
        success, data, error = self._make_request("GET", "/health")
        if success:
            return True, None
        return False, error
    
    def analyze_event(self, event_description: str, top_k: int = 3) -> tuple[bool, Any, Optional[str]]:
        """
        Analyze event and extract themes.
        
        Args:
            event_description (str): Event description
            top_k (int): Number of top themes to return
        
        Returns:
            tuple: (success, response_data, error_message)
        """
        payload = {
            "event_description": event_description,
            "top_k": top_k
        }
        return self._make_request("POST", "/analyze-event", payload)
    
    def generate_conversation(
        self,
        event_description: str,
        themes: List[str],
        interests: List[str],
        num_starters: int = 3
    ) -> tuple[bool, Any, Optional[str]]:
        """
        Generate conversation starters.
        
        Args:
            event_description (str): Event description
            themes (List[str]): Extracted themes
            interests (List[str]): User interests
            num_starters (int): Number of starters to generate
        
        Returns:
            tuple: (success, response_data, error_message)
        """
        payload = {
            "event_description": event_description,
            "themes": themes,
            "interests": interests,
            "num_starters": num_starters
        }
        return self._make_request("POST", "/generate-conversation", payload)
    
    def fact_check(self, query: str, max_summary_length: int = 300) -> tuple[bool, Any, Optional[str]]:
        """
        Check facts on Wikipedia.
        
        Args:
            query (str): Topic to fact-check
            max_summary_length (int): Maximum summary length
        
        Returns:
            tuple: (success, response_data, error_message)
        """
        payload = {
            "query": query,
            "max_summary_length": max_summary_length
        }
        return self._make_request("POST", "/fact-check", payload)
    
    def get_history(self) -> tuple[bool, Any, Optional[str]]:
        """
        Retrieve conversation history.
        
        Returns:
            tuple: (success, response_data, error_message)
        """
        return self._make_request("GET", "/history")
    
    def submit_feedback(
        self,
        item_id: str,
        feedback_type: str,
        notes: Optional[str] = None
    ) -> tuple[bool, Any, Optional[str]]:
        """
        Submit user feedback.
        
        Args:
            item_id (str): ID of item to provide feedback for
            feedback_type (str): "thumbs_up" or "thumbs_down"
            notes (str): Optional feedback notes
        
        Returns:
            tuple: (success, response_data, error_message)
        """
        payload = {
            "item_id": item_id,
            "feedback_type": feedback_type,
            "notes": notes or ""
        }
        return self._make_request("POST", "/feedback", payload)


# Initialize API client
api_client = NetworkingAssistantAPI()

# ==================== UI COMPONENTS ====================

def render_header():
    """Render application header."""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🤝 Personalized Networking Assistant</h1>
        <p class="header-subtitle">AI-powered conversation starters for every event</p>
    </div>
    """, unsafe_allow_html=True)


def render_backend_status():
    """Render backend health status."""
    is_healthy, error = api_client.health_check()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if is_healthy:
            st.success("✓ Backend Connected", icon="✅")
        else:
            st.error("✗ Backend Offline", icon="❌")
            if error:
                st.warning(f"Error: {error}")
    
    return is_healthy


def render_conversation_starter(starter: Dict, index: int):
    """
    Render a single conversation starter card.
    
    Args:
        starter (Dict): Starter data with 'id' and 'starter' keys
        index (int): Index for display numbering
    """
    starter_id = starter.get('id', '')
    starter_text = starter.get('starter', '')
    
    st.markdown(f"""
    <div class="starter-card">
        <span class="starter-number">Starter {index}</span><br>
        <div class="starter-text">"{starter_text}"</div>
    </div>
    """, unsafe_allow_html=True)


def render_fact_result(result: Dict):
    """
    Render fact-check result.
    
    Args:
        result (Dict): Fact-check response data
    """
    if result.get('found'):
        st.markdown(f"""
        <div class="fact-result">
            <div class="fact-title">📖 {result.get('title', 'Unknown')}</div>
            <div class="fact-summary">{result.get('summary', 'No summary available')}</div>
            <a href="{result.get('url', '#')}" target="_blank" class="fact-link">Read full article →</a>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"No Wikipedia article found for this topic. Try a more specific search.")


def render_history_entry(entry: Dict, api_client: NetworkingAssistantAPI):
    """
    Render a history entry with expandable details and feedback.
    
    Args:
        entry (Dict): History entry data
        api_client (NetworkingAssistantAPI): API client for feedback submission
    """
    entry_id = entry.get('id', '')
    event_desc = entry.get('event_description', 'Unknown event')
    themes = entry.get('themes', [])
    interests = entry.get('interests', [])
    created_at = entry.get('created_at', 'Unknown date')
    content = entry.get('content', {})
    starters = content.get('conversation_starters', [])
    
    # Parse and format timestamp
    try:
        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        formatted_date = dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        formatted_date = created_at
    
    with st.expander(f"📝 {event_desc[:50]}... ({formatted_date})", expanded=False):
        # Display event details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Themes:**")
            for theme in themes:
                st.markdown(f'<span class="theme-badge">{theme}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**💡 Interests:**")
            for interest in interests:
                st.markdown(f'<span class="theme-badge">{interest}</span>', unsafe_allow_html=True)
        
        st.divider()
        
        # Display conversation starters
        st.markdown("**Generated Conversation Starters:**")
        for idx, starter in enumerate(starters, 1):
            starter_id = starter.get('id', '')
            starter_text = starter.get('starter', '')
            
            st.markdown(f"""
            <div class="starter-card">
                <span class="starter-number">Starter {idx}</span><br>
                <div class="starter-text">"{starter_text}"</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Feedback buttons for this starter
            col_thumbs_up, col_thumbs_down, col_space = st.columns([1, 1, 3])
            
            with col_thumbs_up:
                if st.button("👍 Helpful", key=f"thumbs_up_{starter_id}"):
                    success, _, error = api_client.submit_feedback(
                        item_id=starter_id,
                        feedback_type="thumbs_up",
                        notes="Helpful conversation starter"
                    )
                    if success:
                        st.success("Thanks for the feedback!")
                        st.session_state.feedback_submitted[starter_id] = True
                    else:
                        st.error(f"Could not submit feedback: {error}")
            
            with col_thumbs_down:
                if st.button("👎 Not Helpful", key=f"thumbs_down_{starter_id}"):
                    success, _, error = api_client.submit_feedback(
                        item_id=starter_id,
                        feedback_type="thumbs_down",
                        notes="Not helpful"
                    )
                    if success:
                        st.success("Thanks for the feedback!")
                        st.session_state.feedback_submitted[starter_id] = True
                    else:
                        st.error(f"Could not submit feedback: {error}")


# ==================== PAGE SECTIONS ====================

def render_sidebar():
    """Render application sidebar."""
    with st.sidebar:
        st.markdown("## 📋 Navigation")
        st.markdown("""
        Use the tabs above to navigate between features:
        
        - **Network Starter Generator**: Generate AI-powered conversation starters
        - **Quick Fact Verification**: Verify facts using Wikipedia
        - **Log History & Feedback**: View your past conversations and provide feedback
        """)
        
        st.divider()
        
        st.markdown("## ℹ️ About")
        st.info("""
        This application uses advanced NLP models to help you prepare for networking events:
        
        - **DistilBERT**: Extracts event themes
        - **GPT-2**: Generates natural conversation starters
        - **Wikipedia API**: Verifies facts quickly
        """)
        
        st.divider()
        
        st.markdown("## 🎯 Tips for Success")
        st.markdown("""
        1. Be specific with event descriptions
        2. List your actual interests for better matches
        3. Save feedback to improve suggestions
        4. Use fact verification to prepare talking points
        """)


def tab_conversation_generator():
    """Render the conversation generator tab."""
    st.header("🚀 Network Starter Generator")
    
    st.markdown("""
    Enter details about your networking event and let AI generate tailored 
    conversation starters based on your interests and the event focus.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Event Details")
        event_description = st.text_area(
            "Event Description",
            value=st.session_state.event_description,
            placeholder="e.g., 'AI for Sustainable Cities Conference'",
            height=100,
            help="Describe the networking event you'll be attending"
        )
        st.session_state.event_description = event_description
    
    with col2:
        st.markdown("### Your Profile")
        user_interests = st.text_area(
            "Your Interests (comma-separated)",
            value=st.session_state.user_interests,
            placeholder="e.g., 'climate change, machine learning, urban planning'",
            height=100,
            help="List topics you're interested in discussing"
        )
        st.session_state.user_interests = user_interests
    
    st.divider()
    
    # Generate button
    col_gen, col_clear = st.columns([1, 4])
    
    with col_gen:
        generate_button = st.button("✨ Generate Starters", key="generate_btn", use_container_width=True)
    
    with col_clear:
        if st.button("Clear", key="clear_btn", use_container_width=True):
            st.session_state.event_description = ""
            st.session_state.user_interests = ""
            st.session_state.generated_starters = None
            st.rerun()
    
    # Generate conversation starters
    if generate_button:
        # Validate inputs
        if not event_description.strip():
            st.error("Please enter an event description")
        elif not user_interests.strip():
            st.error("Please enter at least one interest")
        else:
            with st.spinner("🤖 Analyzing event and generating conversation starters..."):
                # Parse interests
                interests_list = [i.strip() for i in user_interests.split(",") if i.strip()]
                
                # First, analyze the event to extract themes
                success, analysis_data, error = api_client.analyze_event(event_description)
                
                if not success:
                    st.error(f"Error analyzing event: {error}")
                else:
                    themes = [t['label'] for t in analysis_data.get('extracted_themes', [])]
                    
                    if not themes:
                        st.warning("Could not extract themes from event description. Using provided interests.")
                        themes = interests_list[:3]
                    
                    # Generate conversation starters
                    success, gen_data, error = api_client.generate_conversation(
                        event_description=event_description,
                        themes=themes,
                        interests=interests_list,
                        num_starters=3
                    )
                    
                    if not success:
                        st.error(f"Error generating starters: {error}")
                    else:
                        st.session_state.generated_starters = gen_data
                        st.session_state.conversation_id = gen_data.get('conversation_id')
                        st.success("✓ Conversation starters generated successfully!")
    
    # Display results
    if st.session_state.generated_starters:
        st.divider()
        st.markdown("### 💬 Generated Conversation Starters")
        
        result_data = st.session_state.generated_starters
        
        # Display event and themes information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Event Themes:**")
            for theme in result_data.get('themes', []):
                st.markdown(f'<span class="theme-badge">{theme}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Your Interests:**")
            for interest in result_data.get('interests', []):
                st.markdown(f'<span class="theme-badge">{interest}</span>', unsafe_allow_html=True)
        
        st.divider()
        
        # Display conversation starters
        starters = result_data.get('conversation_starters', [])
        if starters:
            for idx, starter in enumerate(starters, 1):
                render_conversation_starter(starter, idx)
        else:
            st.info("No conversation starters generated. Please try again.")
        
        # Display copy/save instructions
        st.info("💡 Tip: You can use these starters to initiate conversations at the event. Try personalizing them further!")


def tab_fact_verification():
    """Render the fact verification tab."""
    st.header("🔍 Quick Fact Verification")
    
    st.markdown("""
    Search for quick facts on Wikipedia to prepare talking points and 
    verify information before your networking event.
    """)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Search Topic",
            value=st.session_state.fact_query,
            placeholder="e.g., 'artificial intelligence', 'blockchain', 'sustainable energy'",
            help="Enter a topic to search for on Wikipedia"
        )
        st.session_state.fact_query = query
    
    with col2:
        search_button = st.button("Search", key="search_btn", use_container_width=True)
    
    st.divider()
    
    # Perform search
    if search_button:
        if not query.strip():
            st.error("Please enter a search topic")
        else:
            with st.spinner("🔎 Searching Wikipedia..."):
                success, fact_data, error = api_client.fact_check(query)
                
                if not success:
                    st.error(f"Search error: {error}")
                else:
                    st.session_state.fact_result = fact_data
                    
                    if fact_data.get('error'):
                        st.warning(f"Note: {fact_data.get('error')}")
    
    # Display results
    if st.session_state.fact_result:
        st.markdown("### 📚 Search Results")
        
        result = st.session_state.fact_result
        
        if result.get('found'):
            render_fact_result(result)
            
            # Provide additional context
            st.info("""
            💡 Use this information to:
            - Understand the topic better
            - Prepare talking points
            - Ask informed questions at the event
            - Find common ground with other attendees
            """)
        else:
            st.warning(
                f"No Wikipedia article found for '{st.session_state.fact_query}'. "
                "Try a different search term or break it into smaller topics."
            )


def tab_history_feedback():
    """Render the history and feedback tab."""
    st.header("📊 Conversation History & Feedback")
    
    st.markdown("""
    Review your past networking conversations and provide feedback to help 
    improve the AI's suggestions for future events.
    """)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🔄 Refresh History", use_container_width=True):
            st.session_state.history_data = None
            st.rerun()
    
    st.divider()
    
    # Load history if not already loaded
    if st.session_state.history_data is None:
        with st.spinner("📚 Loading conversation history..."):
            success, history_data, error = api_client.get_history()
            
            if not success:
                st.error(f"Error loading history: {error}")
            else:
                st.session_state.history_data = history_data
    
    # Display history
    if st.session_state.history_data:
        history = st.session_state.history_data
        total_entries = history.get('total_entries', 0)
        entries = history.get('entries', [])
        
        if total_entries == 0:
            st.info(
                "No conversation history yet. Generate some conversation starters "
                "to see them appear here!"
            )
        else:
            st.markdown(f"### 📝 Total Conversations: {total_entries}")
            st.divider()
            
            # Display each history entry
            for entry in entries:
                render_history_entry(entry, api_client)
            
            # Summary statistics
            st.divider()
            st.markdown("### 📈 Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Generations", total_entries)
            
            with col2:
                # Count unique events
                unique_events = len(set(e.get('event_description', '') for e in entries))
                st.metric("Unique Events", unique_events)
            
            with col3:
                # Count total starters
                total_starters = sum(
                    len(e.get('content', {}).get('conversation_starters', []))
                    for e in entries
                )
                st.metric("Total Starters", total_starters)


# ==================== MAIN APPLICATION ====================

def main():
    """Main application entry point."""
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Check backend status
    is_backend_healthy = render_backend_status()
    
    st.divider()
    
    if not is_backend_healthy:
        st.error("""
        ⚠️ **Backend is not responding.** 
        
        Please make sure the FastAPI backend is running:
        ```bash
        cd backend
        python app.py
        # OR
        uvicorn app:app --reload --host 0.0.0.0 --port 8000
        ```
        """)
    else:
        # Create tabs
        tab1, tab2, tab3 = st.tabs([
            "🚀 Network Starter Generator",
            "🔍 Quick Fact Verification",
            "📊 Log History & Feedback"
        ])
        
        with tab1:
            tab_conversation_generator()
        
        with tab2:
            tab_fact_verification()
        
        with tab3:
            tab_history_feedback()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.85rem; margin-top: 2rem;">
        <p>🤝 Personalized Networking Assistant | Powered by DistilBERT, GPT-2, and Wikipedia</p>
        <p>Built with FastAPI & Streamlit | © 2024</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
