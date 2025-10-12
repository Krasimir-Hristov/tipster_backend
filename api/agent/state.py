"""
Graph State Definition

Defines the state structure that flows through the LangGraph.
This is the "memory" of our agent.
"""

from typing import TypedDict, List, Optional, Dict, Any


class GraphState(TypedDict):
    """
    State structure for the football match analysis workflow.
    
    All data collected and generated during the analysis process
    is stored in this state object.
    """
    # Input data
    team1: str  # Name of the first team
    team2: str  # Name of the second team
    
    # Research data collected from web search
    research_data: Optional[str]  # Raw information from Tavily search
    
    # Structured data for frontend visualization (NEW)
    team1_stats: Optional[Dict[str, Any]]  # Team1 recent matches, form, stats
    team2_stats: Optional[Dict[str, Any]]  # Team2 recent matches, form, stats
    head_to_head: Optional[Dict[str, Any]]  # H2H history and stats
    
    # Analysis results from specialized agents
    goals_analysis: Optional[str]  # Analysis of expected goals count
    winner_analysis: Optional[str]  # Analysis of match winner
    score_analysis: Optional[str]  # Analysis of exact score prediction
    
    # Final aggregated result
    final_analysis: Optional[str]  # Final comprehensive analysis
    
    # Conversation history for chat functionality
    messages: List[dict]  # Chat messages for follow-up questions
