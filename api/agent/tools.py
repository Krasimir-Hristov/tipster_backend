"""
Data Collection Tools

Functions for gathering information about football matches
from various sources (Tavily, API-Football, etc.)
"""

import os
from tavily import TavilyClient
from api.agent.state import GraphState


def search_web_tavily(state: GraphState) -> GraphState:
    """
    Searches the web for recent information using Tavily API.
    
    Gathers:
    - Recent news about both teams
    - Injury reports
    - Team form and performance
    - Head-to-head history
    - Expert predictions
    
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
        print("\n" + "="*80)
        print(f"[TAVILY SEARCH] Gathering data for {team1} vs {team2}")
        print("="*80)
        
        # Initialize Tavily client
        tavily = TavilyClient(api_key=tavily_api_key)
        
        # Construct search query
        query = f"{team1} vs {team2} football match prediction news injuries form statistics"
        
        # Perform search (max 5 results to stay within limits)
        search_results = tavily.search(
            query=query,
            max_results=5,
            search_depth="advanced"
        )
        
        print(f"[OK] Found {len(search_results.get('results', []))} sources:\n")
        
        # Format the results
        formatted_data = f"=== Research Data for {team1} vs {team2} ===\n\n"
        
        if search_results and 'results' in search_results:
            for idx, result in enumerate(search_results['results'], 1):
                title = result.get('title', 'N/A')
                url = result.get('url', 'N/A')
                print(f"   {idx}. {title}")
                print(f"      URL: {url}\n")
                
                formatted_data += f"{idx}. {title}\n"
                formatted_data += f"   Source: {url}\n"
                formatted_data += f"   {result.get('content', 'No content available')}\n\n"
        else:
            formatted_data += "No relevant information found.\n"
            print("   [WARNING] No results found\n")
        
        state["research_data"] = formatted_data
        print("[OK] Tavily search completed\n")
        
    except Exception as e:
        error_msg = f"Error during web search: {str(e)}"
        state["research_data"] = error_msg
        print(f"[ERROR] {error_msg}\n")
    
    return state


def get_football_data(state: GraphState) -> GraphState:
    """
    Fetches structured football data from API-Football.
    
    This is a placeholder for future implementation.
    Will retrieve:
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
    api_key = os.getenv("API_FOOTBALL_KEY")
    
    if not api_key:
        # If no API key, skip this data source
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
        print(f"[WARNING] API-Football error: {str(e)}")
    
    return state
