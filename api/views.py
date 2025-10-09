from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def analyze_teams(request):
    """
    This view will receive the team names,
    trigger the LangGraph agent, and return the analysis.
    """
    # For now, just return a dummy response
    team1 = request.data.get('team1', 'Team A')
    team2 = request.data.get('team2', 'Team B')
    
    return Response({
        "message": f"Analysis for {team1} vs {team2} will be here."
    })
