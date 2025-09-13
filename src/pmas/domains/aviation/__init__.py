"""
Aviation domain package for flight planning and aviation-specific workflows.
"""

from . import constants
from .adapters import (
    AviationLoginAdapter,
    AviationWorkflowOrchestrator,
    FlightPlanAdapter,
    FlightPlanData,
    TankeringAdapter,
    UserCredentials,
    WeatherAdapter,
)
from .pages import BaseAviationPage, LoginPage

__all__ = [
    # Page objects
    "LoginPage",
    "BaseAviationPage",
    # Adapters
    "AviationLoginAdapter",
    "FlightPlanAdapter",
    "TankeringAdapter",
    "WeatherAdapter",
    "AviationWorkflowOrchestrator",
    # Data structures
    "FlightPlanData",
    "UserCredentials",
    # Constants module
    "constants",
]
