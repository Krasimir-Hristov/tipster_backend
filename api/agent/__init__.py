"""
AI Agent for Football Match Analysis

This package contains all the logic for analyzing football matches
using LangGraph and multiple specialized LLM agents.
"""

from api.agent.graph import analysis_graph
from api.agent.state import GraphState

__all__ = ['analysis_graph', 'GraphState']
