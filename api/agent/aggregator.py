"""
Main Aggregator

The powerful AI agent that synthesizes all specialized analyses
into a final comprehensive prediction.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from api.agent.state import GraphState


def aggregate_analysis(state: GraphState) -> GraphState:
    """
    Aggregates all specialized analyses into a final prediction.
    
    Uses Gemini 2.0 Flash Thinking (powerful model) to synthesize
    all information and provide a well-reasoned final analysis.
    
    Args:
        state: Current graph state with all analyses completed
        
    Returns:
        Updated state with final_analysis populated
    """
    team1 = state.get("team1", "")
    team2 = state.get("team2", "")
    research_data = state.get("research_data", "")
    goals_analysis = state.get("goals_analysis", "")
    winner_analysis = state.get("winner_analysis", "")
    score_analysis = state.get("score_analysis", "")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        state["final_analysis"] = "Error: Google API key not configured."
        return state
    
    try:
        # Initialize the powerful Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-thinking-exp",
            google_api_key=google_api_key,
            temperature=0.7  # Higher temperature for creative synthesis
        )
        
        # Comprehensive prompt for final aggregation
        prompt = f"""You are an expert football analyst tasked with providing a FINAL, COMPREHENSIVE match prediction.

Match: {team1} vs {team2}

You have received the following specialized analyses from your team of analysts:

=== RESEARCH DATA ===
{research_data}

=== GOALS ANALYSIS ===
{goals_analysis}

=== WINNER ANALYSIS ===
{winner_analysis}

=== SCORE PREDICTION ===
{score_analysis}

===

Your task is to:
1. SYNTHESIZE all the above information
2. IDENTIFY any contradictions or agreements between the analyses
3. WEIGH the reliability of each prediction based on the research data
4. Provide a FINAL, WELL-REASONED prediction

Your response should include:
- A brief overview of key factors influencing the match
- Your final prediction on the winner
- Your final prediction on the score
- Your confidence level (High/Medium/Low) and reasoning
- Any important caveats or risk factors

Be concise but thorough. Focus on actionable insights.
"""
        
        print("="*80)
        print("[MAIN AGGREGATOR] Gemini 2.0 Flash Thinking: Processing...")
        print("="*80)
        
        response = llm.invoke(prompt)
        state["final_analysis"] = response.content
        
        print("[FINAL ANALYSIS]")
        print("="*80)
        print(response.content)
        print("="*80 + "\n")
        
    except Exception as e:
        error_msg = f"Error in final analysis aggregation: {str(e)}"
        state["final_analysis"] = error_msg
        print(f"[ERROR] {error_msg}\n")
    
    return state
