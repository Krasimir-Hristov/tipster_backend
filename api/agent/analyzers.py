"""
Specialized Analyzers

Three focused analyzers using Gemini Flash for:
- Goals prediction
- Winner prediction  
- Score prediction
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from api.agent.state import GraphState


def analyze_goals(state: GraphState) -> GraphState:
    """
    Analyzes the expected number of goals in the match.
    
    Uses Gemini Flash (cheap, fast model) with a specialized prompt.
    
    Args:
        state: Current graph state with research_data
        
    Returns:
        Updated state with goals_analysis populated
    """
    team1 = state.get("team1", "")
    team2 = state.get("team2", "")
    research_data = state.get("research_data", "")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        state["goals_analysis"] = "Error: Google API key not configured."
        return state
    
    try:
        # Initialize Gemini Flash
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=google_api_key,
            temperature=0.3
        )
        
        # Craft specialized prompt
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
        
        print("="*80)
        print("[GOALS ANALYZER] Gemini Flash: Processing...")
        print("="*80)
        
        response = llm.invoke(prompt)
        state["goals_analysis"] = response.content
        
        print("[GOALS ANALYSIS RESULT]")
        print("-" * 80)
        print(response.content)
        print("-" * 80 + "\n")
        
    except Exception as e:
        error_msg = f"Error in goals analysis: {str(e)}"
        state["goals_analysis"] = error_msg
        print(f"[ERROR] {error_msg}\n")
    
    return state


def analyze_winner(state: GraphState) -> GraphState:
    """
    Analyzes which team is likely to win the match.
    
    Uses Gemini Flash with a specialized prompt for match outcome.
    
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
        
        print("="*80)
        print("[WINNER ANALYZER] Gemini Flash: Processing...")
        print("="*80)
        
        response = llm.invoke(prompt)
        state["winner_analysis"] = response.content
        
        print("[WINNER ANALYSIS RESULT]")
        print("-" * 80)
        print(response.content)
        print("-" * 80 + "\n")
        
    except Exception as e:
        error_msg = f"Error in winner analysis: {str(e)}"
        state["winner_analysis"] = error_msg
        print(f"[ERROR] {error_msg}\n")
    
    return state


def analyze_score(state: GraphState) -> GraphState:
    """
    Predicts the exact score of the match.
    
    Uses Gemini Flash for precise score prediction.
    
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
        
        print("="*80)
        print("[SCORE ANALYZER] Gemini Flash: Processing...")
        print("="*80)
        
        response = llm.invoke(prompt)
        state["score_analysis"] = response.content
        
        print("[SCORE ANALYSIS RESULT]")
        print("-" * 80)
        print(response.content)
        print("-" * 80 + "\n")
        
    except Exception as e:
        error_msg = f"Error in score analysis: {str(e)}"
        state["score_analysis"] = error_msg
        print(f"[ERROR] {error_msg}\n")
    
    return state
