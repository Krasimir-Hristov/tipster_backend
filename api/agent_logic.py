"""
AI Agent Logic for Football Match Analysis

This module contains the LangGraph implementation for analyzing football matches.
It orchestrates multiple specialized LLM agents that work together to provide
comprehensive match predictions.
"""

from typing import TypedDict, List, Optional
from typing_extensions import Annotated
import os
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI


class GraphState(TypedDict):
    """
    Defines the state structure that flows through the LangGraph.
    
    This is the "memory" of our agent - all data collected and generated
    during the analysis process is stored here.
    """
    # Input data
    team1: str  # Name of the first team
    team2: str  # Name of the second team
    
    # Research data collected from web search
    research_data: Optional[str]  # Raw information from Tavily search
    
    # Analysis results from specialized agents
    goals_analysis: Optional[str]  # Analysis of expected goals count
    winner_analysis: Optional[str]  # Analysis of match winner
    score_analysis: Optional[str]  # Analysis of exact score prediction
    
    # Final aggregated result
    final_analysis: Optional[str]  # Final comprehensive analysis from the main LLM
    
    # Conversation history for chat functionality
    messages: List[dict]  # Chat messages for follow-up questions


# ============================================================================
# DATA COLLECTION FUNCTIONS (TOOLS)
# ============================================================================

def search_web_tavily(state: GraphState) -> GraphState:
    """
    Searches the web for recent information about the two teams using Tavily API.
    
    This function gathers:
    - Recent news about both teams
    - Injury reports
    - Team form and performance
    - Head-to-head history
    - Expert predictions and analysis
    
    Args:
        state: Current graph state containing team names
        
    Returns:
        Updated state with research_data populated
    """
    team1 = state.get("team1", "")
    team2 = state.get("team2", "")
    
    # Get Tavily API key from environment
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if not tavily_api_key:
        state["research_data"] = "Error: Tavily API key not configured."
        return state
    
    try:
        # Initialize Tavily client
        tavily = TavilyClient(api_key=tavily_api_key)
        
        # Construct search query for comprehensive football match information
        query = f"{team1} vs {team2} football match prediction news injuries form statistics"
        
        # Perform search (max 5 results to stay within limits)
        search_results = tavily.search(
            query=query,
            max_results=5,
            search_depth="advanced"  # More comprehensive search
        )
        
        # Format the results into readable text
        formatted_data = f"=== Research Data for {team1} vs {team2} ===\n\n"
        
        if search_results and 'results' in search_results:
            for idx, result in enumerate(search_results['results'], 1):
                formatted_data += f"{idx}. {result.get('title', 'N/A')}\n"
                formatted_data += f"   Source: {result.get('url', 'N/A')}\n"
                formatted_data += f"   {result.get('content', 'No content available')}\n\n"
        else:
            formatted_data += "No relevant information found.\n"
        
        state["research_data"] = formatted_data
        
    except Exception as e:
        state["research_data"] = f"Error during web search: {str(e)}"
    
    return state


def get_football_data(state: GraphState) -> GraphState:
    """
    Fetches structured football data from API-Football.
    
    This is a placeholder function that will retrieve:
    - Team statistics
    - Head-to-head records
    - Recent match results
    - Player injuries and suspensions
    
    Args:
        state: Current graph state containing team names
        
    Returns:
        Updated state with additional structured data
        
    Note:
        Requires API_FOOTBALL_KEY in environment variables.
        Get your free key at: https://www.api-football.com/
    """
    team1 = state.get("team1", "")
    team2 = state.get("team2", "")
    
    api_key = os.getenv("API_FOOTBALL_KEY")
    
    if not api_key:
        # If no API key, just skip this data source
        # The Tavily search will still provide valuable information
        return state
    
    try:
        # TODO: Implement API-Football integration here
        # Example structure:
        # 1. Search for team IDs
        # 2. Get head-to-head statistics
        # 3. Get recent form (last 5 matches)
        # 4. Get injury/suspension list
        # 5. Append to research_data
        
        pass
        
    except Exception as e:
        # Don't fail the entire flow if this API is down
        print(f"API-Football error: {str(e)}")
    
    return state


# ============================================================================
# SPECIALIZED ANALYZER NODES (Using Cheap LLM - Gemini Flash)
# ============================================================================

def analyze_goals(state: GraphState) -> GraphState:
    """
    Analyzes the expected number of goals in the match.
    
    Uses Gemini Flash (cheap, fast model) with a specialized prompt
    to predict goal count based on collected research data.
    
    Args:
        state: Current graph state with research_data
        
    Returns:
        Updated state with goals_analysis populated
    """
    team1 = state.get("team1", "")
    team2 = state.get("team2", "")
    research_data = state.get("research_data", "")
    
    # Get Google API key
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        state["goals_analysis"] = "Error: Google API key not configured."
        return state
    
    try:
        # Initialize the cheap Gemini Flash model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=google_api_key,
            temperature=0.3  # Lower temperature for more focused analysis
        )
        
        # Craft a specialized prompt for goals analysis
        prompt = f"""You are a football match analyst specializing in GOAL PREDICTIONS.

Match: {team1} vs {team2}

Research Data:
{research_data}

Based on the above information, analyze and predict the TOTAL NUMBER OF GOALS in this match.

Consider:
- Recent scoring form of both teams
- Defensive records
- Head-to-head goal statistics
- Playing styles (attacking vs defensive)
- Injuries to key attackers or defenders

Provide your analysis in 2-3 concise sentences, ending with a specific prediction:
"Expected goals: Over/Under 2.5" or "Expected goals: 2-3 total"
"""
        
        # Get the analysis from the LLM
        response = llm.invoke(prompt)
        state["goals_analysis"] = response.content
        
    except Exception as e:
        state["goals_analysis"] = f"Error in goals analysis: {str(e)}"
    
    return state


def analyze_winner(state: GraphState) -> GraphState:
    """
    Analyzes which team is likely to win the match.
    
    Uses Gemini Flash with a specialized prompt focused on
    match outcome prediction.
    
    Args:
        state: Current graph state with research_data
        
    Returns:
        Updated state with winner_analysis populated
    """
    team1 = state.get("team1", "")
    team2 = state.get("team2", "")
    research_data = state.get("research_data", "")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        state["winner_analysis"] = "Error: Google API key not configured."
        return state
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=google_api_key,
            temperature=0.3
        )
        
        prompt = f"""You are a football match analyst specializing in MATCH OUTCOME predictions.

Match: {team1} vs {team2}

Research Data:
{research_data}

Based on the above information, predict the WINNER of this match.

Consider:
- Current form and momentum
- Home advantage (if applicable)
- Head-to-head record
- Team morale and recent results
- Key player availability

Provide your analysis in 2-3 concise sentences, ending with a clear prediction:
"{team1} to win", "{team2} to win", or "Draw likely"
"""
        
        response = llm.invoke(prompt)
        state["winner_analysis"] = response.content
        
    except Exception as e:
        state["winner_analysis"] = f"Error in winner analysis: {str(e)}"
    
    return state


def analyze_score(state: GraphState) -> GraphState:
    """
    Predicts the exact score of the match.
    
    Uses Gemini Flash with a specialized prompt for
    precise score prediction.
    
    Args:
        state: Current graph state with research_data
        
    Returns:
        Updated state with score_analysis populated
    """
    team1 = state.get("team1", "")
    team2 = state.get("team2", "")
    research_data = state.get("research_data", "")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        state["score_analysis"] = "Error: Google API key not configured."
        return state
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=google_api_key,
            temperature=0.3
        )
        
        prompt = f"""You are a football match analyst specializing in EXACT SCORE predictions.

Match: {team1} vs {team2}

Research Data:
{research_data}

Based on the above information, predict the EXACT FINAL SCORE of this match.

Consider:
- Typical score patterns for these teams
- Recent match scores
- Offensive and defensive capabilities
- Historical score lines in similar matchups

Provide your analysis in 2-3 concise sentences, ending with a specific score prediction:
"Predicted score: {team1} 2-1 {team2}" (use actual team names)
"""
        
        response = llm.invoke(prompt)
        state["score_analysis"] = response.content
        
    except Exception as e:
        state["score_analysis"] = f"Error in score analysis: {str(e)}"
    
    return state
