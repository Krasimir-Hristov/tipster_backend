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
        
        # SEARCH 1: Direct match prediction and head-to-head
        query1 = f"{team1} vs {team2} football match prediction latest results goals scored recent form head to head statistics injuries lineup"
        
        print(f"[SEARCH 1 - Match Specific] {query1}\n")
        
        search_results1 = tavily.search(
            query=query1,
            max_results=3,
            search_depth="advanced",
            include_domains=["flashscore.com", "sofascore.com", "espn.com", "bbc.com", "uefa.com", "fifa.com", "transfermarkt.com", "footballwhispers.com", "whoscored.com"]
        )
        
        # SEARCH 2: Recent form of team1
        query2 = f"{team1} football recent results last 5 matches goals scored form statistics 2025"
        
        print(f"[SEARCH 2 - {team1} Recent Form] {query2}\n")
        
        search_results2 = tavily.search(
            query=query2,
            max_results=2,
            search_depth="basic"
        )
        
        # SEARCH 3: Recent form of team2
        query3 = f"{team2} football recent results last 5 matches goals scored form statistics 2025"
        
        print(f"[SEARCH 3 - {team2} Recent Form] {query3}\n")
        
        search_results3 = tavily.search(
            query=query3,
            max_results=2,
            search_depth="basic"
        )
        
        # Combine all results
        all_results = []
        if search_results1 and 'results' in search_results1:
            all_results.extend(search_results1['results'])
        if search_results2 and 'results' in search_results2:
            all_results.extend(search_results2['results'])
        if search_results3 and 'results' in search_results3:
            all_results.extend(search_results3['results'])
        
        print(f"[OK] Found {len(all_results)} total sources across all searches\n")
        
        # Format the results
        formatted_data = f"=== Research Data for {team1} vs {team2} ===\n\n"
        
        if all_results:
            for idx, result in enumerate(all_results, 1):
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
        print("[OK] All Tavily searches completed\n")
        
    except (ValueError, KeyError, ConnectionError) as e:
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
        
    except (ValueError, KeyError, ConnectionError) as e:
        # Don't fail the entire flow if this API is down
        print(f"[WARNING] API-Football error: {str(e)}")
    
    return state
