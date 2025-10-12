"""
Data Parser Module

Extracts structured data from raw research text using LLM-based parsing.
Converts unstructured Tavily search results into structured JSON for frontend visualization.
"""

import os
import json
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from api.agent.state import GraphState


def parse_structured_data(state: GraphState) -> GraphState:
    """
    Parses research_data to extract structured information:
    - Team1 recent matches (last 10)
    - Team2 recent matches (last 10)
    - Head-to-head history (last 10)
    
    Uses Gemini Flash to convert text to structured JSON.
    """
    team1 = state.get("team1", "")
    team2 = state.get("team2", "")
    research_data = state.get("research_data", "")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        print("[ERROR] Google API key not configured for parsing")
        state["team1_stats"] = {"error": "API key not configured"}
        state["team2_stats"] = {"error": "API key not configured"}
        state["head_to_head"] = {"error": "API key not configured"}
        return state
    
    if not research_data or research_data == "No relevant information found.":
        print("[WARNING] No research data available for parsing")
        state["team1_stats"] = {"error": "Няма достатъчно информация"}
        state["team2_stats"] = {"error": "Няма достатъчно информация"}
        state["head_to_head"] = {"error": "Няма достатъчно информация"}
        return state
    
    try:
        print("\n" + "="*80)
        print("[PARSER] Extracting structured data with Gemini Flash...")
        print("="*80)
        
        # Initialize Gemini for parsing
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=google_api_key,
            temperature=0.1  # Low temperature for factual extraction
        )
        
        # Parsing prompt
        prompt = f"""You are a data extraction specialist. Extract structured football match data from the provided research text.

Match: {team1} vs {team2}

Research Data:
{research_data}

Your task: Extract and format the following information as valid JSON:

1. **{team1} Recent Matches** (last 10 if available):
   - Each match should have: date, opponent, score, home_away, result (win/loss/draw), goals_scored, goals_conceded
   
2. **{team2} Recent Matches** (last 10 if available):
   - Same structure as above

3. **Head-to-Head History** (last 10 matches between {team1} and {team2}):
   - Each match: date, home_team, away_team, score, winner

4. **Summary Statistics**:
   - For each team: form (e.g., "WWLDW"), total goals scored in last matches, total goals conceded, average goals

CRITICAL INSTRUCTIONS:
- Extract ONLY information that is EXPLICITLY stated in the research data
- If a field is not available, use null
- If fewer than 10 matches are found, return only what's available
- Dates should be in YYYY-MM-DD format if possible, otherwise use the format provided
- Scores should be in "X-Y" format (e.g., "3-1")
- For home_away use "home" or "away"
- For result use "win", "loss", or "draw"
- Form should be a string like "WWLDW" (W=win, L=loss, D=draw) based on most recent to oldest

Return ONLY valid JSON in this exact structure (no markdown, no explanations):

{{
  "team1_stats": {{
    "name": "{team1}",
    "recent_matches": [
      {{
        "date": "2025-10-11",
        "opponent": "Opponent Name",
        "score": "2-1",
        "home_away": "home",
        "result": "win",
        "goals_scored": 2,
        "goals_conceded": 1
      }}
    ],
    "form": "WWLDW",
    "total_goals_scored": 15,
    "total_goals_conceded": 5,
    "avg_goals_scored": 1.5,
    "avg_goals_conceded": 0.5,
    "matches_analyzed": 10
  }},
  "team2_stats": {{
    "name": "{team2}",
    "recent_matches": [ /* same structure */ ],
    "form": "LLDWL",
    "total_goals_scored": 8,
    "total_goals_conceded": 20,
    "avg_goals_scored": 0.8,
    "avg_goals_conceded": 2.0,
    "matches_analyzed": 10
  }},
  "head_to_head": {{
    "total_matches": 5,
    "team1_wins": 3,
    "draws": 1,
    "team2_wins": 1,
    "recent_matches": [
      {{
        "date": "2025-10-11",
        "home_team": "{team1}",
        "away_team": "{team2}",
        "score": "2-1",
        "winner": "{team1}"
      }}
    ]
  }}
}}

If insufficient data exists for a section, use:
{{
  "error": "Няма достатъчно информация",
  "available_data": /* any partial data found */
}}
"""
        
        print("[PARSER] Sending extraction request to Gemini...")
        response = llm.invoke(prompt)
        response_text = response.content.strip()
        
        # Try to extract JSON from response
        # Sometimes LLM wraps JSON in markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        print(f"[PARSER] Raw response length: {len(response_text)} chars")
        
        # Parse JSON
        parsed_data = json.loads(response_text)
        
        # Validate and assign to state
        state["team1_stats"] = parsed_data.get("team1_stats", {"error": "Parsing failed"})
        state["team2_stats"] = parsed_data.get("team2_stats", {"error": "Parsing failed"})
        state["head_to_head"] = parsed_data.get("head_to_head", {"error": "Parsing failed"})
        
        # Print summary
        print("\n[PARSER] Extraction Results:")
        team1_matches = len(state["team1_stats"].get("recent_matches", []))
        team2_matches = len(state["team2_stats"].get("recent_matches", []))
        h2h_matches = len(state["head_to_head"].get("recent_matches", []))
        
        print(f"  • {team1} recent matches: {team1_matches}")
        print(f"  • {team2} recent matches: {team2_matches}")
        print(f"  • Head-to-head matches: {h2h_matches}")
        
        if team1_matches > 0:
            print(f"  • {team1} form: {state['team1_stats'].get('form', 'N/A')}")
        if team2_matches > 0:
            print(f"  • {team2} form: {state['team2_stats'].get('form', 'N/A')}")
        
        print("[OK] Structured data extraction completed\n")
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parsing failed: {e}")
        print(f"[ERROR] Response was: {response_text[:500]}...")
        state["team1_stats"] = {"error": "Грешка при обработка на данните"}
        state["team2_stats"] = {"error": "Грешка при обработка на данните"}
        state["head_to_head"] = {"error": "Грешка при обработка на данните"}
    except Exception as e:
        print(f"[ERROR] Data extraction failed: {e}")
        state["team1_stats"] = {"error": "Няма достатъчно информация"}
        state["team2_stats"] = {"error": "Няма достатъчно информация"}
        state["head_to_head"] = {"error": "Няма достатъчно информация"}
    
    return state
