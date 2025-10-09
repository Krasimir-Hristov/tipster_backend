from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .agent_logic import analysis_graph

@api_view(['POST'])
def analyze_teams(request):
    """
    This view receives team names, triggers the LangGraph agent,
    and returns the complete AI analysis.
    
    Expected POST body:
    {
        "team1": "Real Madrid",
        "team2": "Barcelona"
    }
    
    Returns:
    {
        "team1": "Real Madrid",
        "team2": "Barcelona",
        "analysis": {
            "goals_prediction": "...",
            "winner_prediction": "...",
            "score_prediction": "...",
            "final_analysis": "...",
            "research_data": "..."
        }
    }
    """
    try:
        # Get team names from request
        team1 = request.data.get('team1')
        team2 = request.data.get('team2')
        
        # Validate input
        if not team1 or not team2:
            return Response({
                "error": "Both team1 and team2 are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare initial state for the graph
        initial_state = {
            "team1": team1,
            "team2": team2,
            "research_data": "",
            "goals_analysis": "",
            "winner_analysis": "",
            "score_analysis": "",
            "final_analysis": "",
            "messages": []
        }
        
        # Run the LangGraph workflow
        # This will execute: gather_data -> analyzers (parallel) -> aggregate
        result = analysis_graph.invoke(initial_state)
        
        # Format the response for the Next.js frontend
        response_data = {
            "team1": team1,
            "team2": team2,
            "analysis": {
                "goals_prediction": result.get("goals_analysis", ""),
                "winner_prediction": result.get("winner_analysis", ""),
                "score_prediction": result.get("score_analysis", ""),
                "final_analysis": result.get("final_analysis", ""),
                "research_data": result.get("research_data", "")
            },
            "success": True
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Handle any errors gracefully
        return Response({
            "error": f"An error occurred during analysis: {str(e)}",
            "success": False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
