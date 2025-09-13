"""
Manufacturing domain package for production planning and manufacturing workflows.
"""

from . import constants
from .adapters import (
    ManufacturingLoginAdapter,
    ManufacturingUserCredentials,
    ManufacturingWorkflowOrchestrator,
    MaterialPlanningAdapter,
    ProductionOrderAdapter,
    ProductionOrderData,
    QualityControlAdapter,
)
from .pages import BaseManufacturingPage, ManufacturingLoginPage

__all__ = [
    # Page objects
    "ManufacturingLoginPage",
    "BaseManufacturingPage",
    # Adapters
    "ManufacturingLoginAdapter",
    "ProductionOrderAdapter",
    "MaterialPlanningAdapter",
    "QualityControlAdapter",
    "ManufacturingWorkflowOrchestrator",
    # Data structures
    "ProductionOrderData",
    "ManufacturingUserCredentials",
    # Constants module
    "constants",
]
