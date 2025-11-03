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

IMPORTANT: You MUST respond ENTIRELY in GERMAN language. All your analysis, predictions, and explanations must be in German.

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

CRITICAL INSTRUCTIONS:
1. Pay SPECIAL attention to RECENT ACTUAL MATCH RESULTS in the research data
2. If one team recently scored 6+ goals, they are in EXCEPTIONAL form - reflect this!
3. If one team recently conceded many goals, their defense is weak - factor this heavily!
4. Don't be conservative if recent results show dominant performances
5. Large recent score differences (e.g., 6-1, 5-0) are STRONG indicators of current form disparity

Your task is to:
1. SYNTHESIZE all the above information, prioritizing RECENT ACTUAL RESULTS
2. IDENTIFY any contradictions or agreements between the analyses
3. WEIGH the reliability of each prediction based on the research data (recent results are most reliable!)
4. Provide a FINAL, WELL-REASONED prediction IN GERMAN that reflects current form

Your response IN GERMAN should include:
- Kurzer Überblick über die Schlüsselfaktoren, die das Spiel beeinflussen (besonders aktuelle Form!)
- Finale Prognose für den Gewinner
- Finale Prognose für das Ergebnis (scheue dich nicht, 3-0, 4-1, 5-0 vorherzusagen, wenn die Daten es zeigen!)
- Vertrauensniveau (Hoch/Mittel/Niedrig) und Erklärung
- Wichtige Warnungen oder Risikofaktoren

Be bold with predictions when recent data shows clear dominance. Focus on actionable insights. REMEMBER: Write EVERYTHING in GERMAN!
"""
        
        print("="*80)
        print("[MAIN AGGREGATOR] Gemini 2.0 Flash Thinking: Processing...")
        print("="*80)
        
        response = llm.invoke(prompt)
        # Ensure content is string
        content = response.content if isinstance(response.content, str) else str(response.content)
        state["final_analysis"] = content
        
        print("[FINAL ANALYSIS]")
        print("="*80)
        print(content)
        print("="*80 + "\n")
        
    except (ValueError, KeyError, AttributeError) as e:
        error_msg = f"Error in final analysis aggregation: {str(e)}"
        state["final_analysis"] = error_msg
        print(f"[ERROR] {error_msg}\n")
    
    return state
