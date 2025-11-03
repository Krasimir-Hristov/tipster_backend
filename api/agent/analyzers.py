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
        # Initialize Gemini Pro (higher rate limits)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=google_api_key,
            temperature=0.3
        )
        
        # Craft specialized prompt
        prompt = f"""You are a football match analyst specializing in GOAL PREDICTIONS.

IMPORTANT: You must respond in BULGARIAN language.

Match: {team1} vs {team2}

Research Data:
{research_data}

Based on the above information, analyze and predict the TOTAL NUMBER OF GOALS in this match.

CRITICAL: Pay special attention to:
- RECENT match results and actual goals scored (last 3-5 games for each team)
- If one team scored 6+ goals recently, they are in EXCEPTIONAL attacking form
- Historical head-to-head results and goal patterns
- Large score differences in recent matches indicate current form disparity
- Defensive records - teams conceding many goals recently will likely continue

Consider:
- Recent scoring form of both teams (MOST IMPORTANT - actual recent results!)
- Defensive records and recent goals conceded
- Head-to-head goal statistics and historical score patterns
- Playing styles (attacking vs defensive)
- Injuries to key attackers or defenders

If recent matches show high-scoring games (4+ goals), predict accordingly. Don't be conservative if data shows attacking dominance.

Provide your analysis in BULGARIAN in 2-3 concise sentences, ending with a specific prediction:
"Очаквани голове: Over/Under 2.5" or "Очаквани голове: 2-3 общо" or "Очаквани голове: 4+ общо" (adapt based on recent form!)
"""
        
        print("="*80)
        print("[GOALS ANALYZER] Gemini Flash: Processing...")
        print("="*80)
        
        response = llm.invoke(prompt)
        # Ensure content is string (LangChain can return str or list)
        content = response.content if isinstance(response.content, str) else str(response.content)
        state["goals_analysis"] = content
        
        print("[GOALS ANALYSIS RESULT]")
        print("-" * 80)
        print(content)
        print("-" * 80 + "\n")
        
    except (ValueError, KeyError, AttributeError) as e:
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

IMPORTANT: You must respond in BULGARIAN language.

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

Provide your analysis in BULGARIAN in 2-3 concise sentences, ending with a clear prediction:
"{team1} ще спечели", "{team2} ще спечели", или "Вероятна е равен резултат"
"""
        
        print("="*80)
        print("[WINNER ANALYZER] Gemini Flash: Processing...")
        print("="*80)
        
        response = llm.invoke(prompt)
        # Ensure content is string
        content = response.content if isinstance(response.content, str) else str(response.content)
        state["winner_analysis"] = content
        
        print("[WINNER ANALYSIS RESULT]")
        print("-" * 80)
        print(content)
        print("-" * 80 + "\n")
        
    except (ValueError, KeyError, AttributeError) as e:
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

IMPORTANT: You must respond in BULGARIAN language.

Match: {team1} vs {team2}

Research Data:
{research_data}

Based on the above information, predict the EXACT FINAL SCORE of this match.

CRITICAL: Pay special attention to:
- RECENT actual match results (last 3-5 games) - these show CURRENT form!
- If one team scored 6 goals and the other conceded 6 recently, expect similar patterns
- Head-to-head historical scores between these exact teams
- Large score differences in recent matches (e.g., 6-1, 5-0) indicate current dominance
- Don't predict conservatively if recent results show high-scoring dominant wins

Consider:
- Typical score patterns for these teams IN RECENT GAMES (most important!)
- Recent match scores (actual results from last few games)
- Offensive and defensive capabilities based on RECENT performance
- Historical score lines in similar matchups between these teams
- Current form disparity - if one team is much stronger recently, reflect this!

If recent data shows one team scoring many goals (4+) and the other conceding many, predict a clear win with multiple goals.

Provide your analysis in BULGARIAN in 2-3 concise sentences, ending with a specific score prediction:
"Прогнозиран резултат: {team1} 2-1 {team2}" (използвай истинските имена на отборите)
Adapt the score based on recent form - don't hesitate to predict 3-0, 4-1, etc. if data supports it!
"""
        
        print("="*80)
        print("[SCORE ANALYZER] Gemini Flash: Processing...")
        print("="*80)
        
        response = llm.invoke(prompt)
        # Ensure content is string
        content = response.content if isinstance(response.content, str) else str(response.content)
        state["score_analysis"] = content
        
        print("[SCORE ANALYSIS RESULT]")
        print("-" * 80)
        print(content)
        print("-" * 80 + "\n")
        
    except (ValueError, KeyError, AttributeError) as e:
        error_msg = f"Error in score analysis: {str(e)}"
        state["score_analysis"] = error_msg
        print(f"[ERROR] {error_msg}\n")
    
    return state
