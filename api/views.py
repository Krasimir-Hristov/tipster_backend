from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .agent import analysis_graph

@api_view(['POST'])
def analyze_teams(request):
    """
    This view receives match data from The Odds API, triggers the LangGraph agent,
    and returns the complete AI analysis with structured data.
    
    Expected POST body (from The Odds API):
    {
        "id": "abc123...",
        "sport_key": "soccer_...",
        "commence_time": "2025-10-12T19:00:00Z",
        "home_team": "Real Madrid",
        "away_team": "Barcelona"
    }
    
    Legacy format also supported:
    {
        "team1": "Real Madrid",
        "team2": "Barcelona"
    }
    
    Returns:
    {
        "team1": "Real Madrid",
        "team2": "Barcelona",
        "match_id": "abc123...",
        "commence_time": "2025-10-12T19:00:00Z",
        "analysis": {
            "goals_prediction": "...",
            "winner_prediction": "...",
            "score_prediction": "...",
            "final_analysis": "...",
            "research_data": "..."
        },
        "team1_stats": {...},
        "team2_stats": {...},
        "head_to_head": {...}
    }
    """
    try:
        # Accept The Odds API format (preferred) or legacy format
        match_id = request.data.get('id', None)
        sport_key = request.data.get('sport_key', None)
        commence_time = request.data.get('commence_time', None)
        
        # The Odds API uses home_team/away_team
        home_team = request.data.get('home_team')
        away_team = request.data.get('away_team')
        
        # Legacy format uses team1/team2
        team1 = request.data.get('team1')
        team2 = request.data.get('team2')
        
        # Prefer The Odds API format
        if home_team and away_team:
            team1 = home_team
            team2 = away_team
        
        # Validate input
        if not team1 or not team2:
            return Response({
                "error": "Both teams are required (home_team/away_team or team1/team2)"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare initial state for the graph
        initial_state = {
            "team1": team1,
            "team2": team2,
            "research_data": "",
            "team1_stats": None,  # NEW: Will be populated by parser
            "team2_stats": None,  # NEW: Will be populated by parser
            "head_to_head": None,  # NEW: Will be populated by parser
            "goals_analysis": "",
            "winner_analysis": "",
            "score_analysis": "",
            "final_analysis": "",
            "messages": []
        }
        
        # Run the LangGraph workflow
        # This will execute: gather_data -> parse_data -> analyzers -> aggregate
        result = analysis_graph.invoke(initial_state)
        
        # Format the response for the Next.js frontend
        response_data = {
            "team1": team1,
            "team2": team2,
            "match_id": match_id,  # NEW: The Odds API match ID
            "commence_time": commence_time,  # NEW: Match start time
            "sport_key": sport_key,  # NEW: Sport identifier
            "analysis": {
                "goals_prediction": result.get("goals_analysis", ""),
                "winner_prediction": result.get("winner_analysis", ""),
                "score_prediction": result.get("score_analysis", ""),
                "final_analysis": result.get("final_analysis", ""),
                "research_data": result.get("research_data", "")
            },
            # NEW: Include structured data for frontend visualization
            "team1_stats": result.get("team1_stats", {"error": "Няма достатъчно информация"}),
            "team2_stats": result.get("team2_stats", {"error": "Няма достатъчно информация"}),
            "head_to_head": result.get("head_to_head", {"error": "Няма достатъчно информация"}),
            "success": True
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Handle any errors gracefully
        return Response({
            "error": f"An error occurred during analysis: {str(e)}",
            "success": False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
