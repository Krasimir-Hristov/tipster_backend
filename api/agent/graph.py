"""
LangGraph Workflow Assembly

Creates and compiles the complete workflow for football match analysis.
"""

from langgraph.graph import StateGraph, END
from api.agent.state import GraphState
from api.agent.tools import search_web_tavily
from api.agent.parser import parse_structured_data
from api.agent.analyzers import analyze_goals, analyze_winner, analyze_score
from api.agent.aggregator import aggregate_analysis


def create_analysis_graph():
    """
    Creates and compiles the LangGraph workflow.
    
    Workflow:
    1. Gather data from web (Tavily)
    2. Parse structured data (recent matches, H2H) (Gemini Flash)
    3. Analyze goals (Gemini Flash)
    4. Analyze winner (Gemini Flash)
    5. Analyze score (Gemini Flash)
    6. Aggregate all analyses (Gemini Thinking)
    
    Returns:
        Compiled LangGraph ready to be invoked
    """
    # Initialize the graph
    workflow = StateGraph(GraphState)
    
    # Add all nodes
    workflow.add_node("gather_data", search_web_tavily)
    workflow.add_node("parse_data", parse_structured_data)  # NEW: Parse structured data
    workflow.add_node("analyze_goals", analyze_goals)
    workflow.add_node("analyze_winner", analyze_winner)
    workflow.add_node("analyze_score", analyze_score)
    workflow.add_node("aggregate", aggregate_analysis)
    
    # Define the flow (sequential execution)
    workflow.set_entry_point("gather_data")
    workflow.add_edge("gather_data", "parse_data")  # NEW: Parse after gathering
    workflow.add_edge("parse_data", "analyze_goals")  # Continue to analysis
    workflow.add_edge("analyze_goals", "analyze_winner")
    workflow.add_edge("analyze_winner", "analyze_score")
    workflow.add_edge("analyze_score", "aggregate")
    workflow.add_edge("aggregate", END)
    
    # Compile and return
    return workflow.compile()


# Create singleton instance
analysis_graph = create_analysis_graph()
