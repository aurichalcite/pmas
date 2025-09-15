"""
Aviation domain adapters that compose core components for aviation-specific workflows.
"""

import logging
from dataclasses import dataclass
from typing import Any

from ...config.model import Config
from ...core.driver import WebDriverProtocol
from .pages.base_aviation_page import BaseAviationPage
from .pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@dataclass
class FlightPlanData:
    """Data structure for flight plan information."""

    tail_number: str
    departure: str
    arrival: str
    departure_time: str
    passengers: int
    fuel_required: float
    alternate_1: str | None = None
    alternate_2: str | None = None
    route: str | None = None
    cruise_altitude: str | None = None


@dataclass
class UserCredentials:
    """User credentials for aviation system."""

    username: str
    password: str
    user_type: int
    company: str | None = None


class AviationLoginAdapter:
    """
    Adapter for aviation login workflows.
    Provides high-level login operations for different user types.
    """

    def __init__(self, driver: WebDriverProtocol, config: Config) -> None:
        self.driver = driver
        self.config = config
        self.login_page = LoginPage(
            driver, config.environment.base_url, config.test.default_timeout
        )

    def login_as_regular_user(self) -> BaseAviationPage | None:
        """Login as a regular aviation user."""
        logger.info("Logging in as regular user")
        self.login_page.navigate_to_login()
        return self.login_page.login_reg()

    def login_as_admin(self) -> BaseAviationPage | None:
        """Login as an admin user."""
        logger.info("Logging in as admin user")
        self.login_page.navigate_to_login()
        return self.login_page.login_admin()

    def login_as_flight_coordinator(self) -> BaseAviationPage | None:
        """Login as a flight coordinator."""
        logger.info("Logging in as flight coordinator")
        self.login_page.navigate_to_login()
        return self.login_page.login_fc()

    def login_as_customer(self, username: str | None = None) -> BaseAviationPage | None:
        """Login as a customer user."""
        logger.info(f"Logging in as customer: {username or 'random'}")
        self.login_page.navigate_to_login()
        return self.login_page.login_customer(username)

    def login_with_credentials(
        self, credentials: UserCredentials
    ) -> BaseAviationPage | None:
        """Login with specific credentials."""
        logger.info(f"Logging in with credentials: {credentials.username}")
        self.login_page.navigate_to_login()
        return self.login_page.login(credentials.username, credentials.password)

    def test_invalid_login(self, username: str, attempts: int = 3) -> bool:
        """
        Test invalid login attempts.

        Args:
            username: Username to test
            attempts: Number of invalid attempts

        Returns:
            True if login correctly failed, False otherwise
        """
        logger.info(f"Testing invalid login for user: {username}")
        self.login_page.navigate_to_login()
        result = self.login_page.login_fail(username, attempts)
        return result is None  # None means login failed as expected


class FlightPlanAdapter:
    """
    Adapter for flight planning workflows.
    Provides high-level operations for creating and managing flight plans.
    """

    def __init__(self, driver: WebDriverProtocol, config: Config) -> None:
        self.driver = driver
        self.config = config
        self.current_page: BaseAviationPage | None = None

    def create_flight_plan(self, flight_data: FlightPlanData) -> dict[str, Any]:
        """
        Create a new flight plan.

        Args:
            flight_data: Flight plan data

        Returns:
            Dictionary with creation results
        """
        logger.info(
            f"Creating flight plan: {flight_data.tail_number} "
            f"from {flight_data.departure} to {flight_data.arrival}"
        )

        try:
            # Navigate to Create FPL page
            # This would need actual implementation with the Create FPL page object

            # Fill flight plan form
            # This would use the actual form elements

            # Submit flight plan
            # This would handle the submission process

            return {
                "success": True,
                "flight_plan_id": "FPL123456",  # Placeholder
                "recall_number": "RCL789012",  # Placeholder
                "message": "Flight plan created successfully",
            }

        except Exception as e:
            logger.error(f"Failed to create flight plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Flight plan creation failed",
            }

    def file_flight_plan(self, flight_plan_id: str) -> dict[str, Any]:
        """
        File an existing flight plan.

        Args:
            flight_plan_id: ID of the flight plan to file

        Returns:
            Dictionary with filing results
        """
        logger.info(f"Filing flight plan: {flight_plan_id}")

        try:
            # Implementation would go here
            return {
                "success": True,
                "filed_time": "2024-01-15 14:00:00",
                "message": "Flight plan filed successfully",
            }
        except Exception as e:
            logger.error(f"Failed to file flight plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Flight plan filing failed",
            }

    def check_filing_status(self, recall_number: str) -> dict[str, Any]:
        """
        Check the filing status of a flight plan.

        Args:
            recall_number: Recall number of the flight plan

        Returns:
            Dictionary with status information
        """
        logger.info(f"Checking filing status for recall: {recall_number}")

        try:
            # Implementation would go here
            return {
                "success": True,
                "status": "FILED",
                "filed_time": "2024-01-15 14:00:00",
                "message": "Status retrieved successfully",
            }
        except Exception as e:
            logger.error(f"Failed to check filing status: {e}")
            return {"success": False, "error": str(e), "message": "Status check failed"}


class TankeringAdapter:
    """
    Adapter for fuel tankering calculations and workflows.
    """

    def __init__(self, driver: WebDriverProtocol, config: Config) -> None:
        self.driver = driver
        self.config = config

    def calculate_tankering(
        self, flight_data: FlightPlanData, fuel_prices: dict[str, float]
    ) -> dict[str, Any]:
        """
        Calculate fuel tankering for a flight.

        Args:
            flight_data: Flight plan data
            fuel_prices: Fuel prices at different airports

        Returns:
            Dictionary with tankering calculations
        """
        logger.info(f"Calculating tankering for flight: {flight_data.tail_number}")

        try:
            # Implementation would navigate to tankering page and perform calculations
            return {
                "success": True,
                "recommended_fuel": 25000,
                "cost_savings": 1500.00,
                "tankering_airport": flight_data.departure,
                "message": "Tankering calculation completed",
            }
        except Exception as e:
            logger.error(f"Failed to calculate tankering: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Tankering calculation failed",
            }


class WeatherAdapter:
    """
    Adapter for weather-related workflows.
    """

    def __init__(self, driver: WebDriverProtocol, config: Config) -> None:
        self.driver = driver
        self.config = config

    def get_weather_briefing(self, airports: list[str]) -> dict[str, Any]:
        """
        Get weather briefing for specified airports.

        Args:
            airports: List of airport codes

        Returns:
            Dictionary with weather information
        """
        logger.info(f"Getting weather briefing for airports: {airports}")

        try:
            # Implementation would navigate to weather pages and collect data
            return {
                "success": True,
                "weather_data": {
                    airport: {
                        "conditions": "VFR",
                        "visibility": "10SM",
                        "wind": "270/10",
                        "temperature": "22C",
                    }
                    for airport in airports
                },
                "message": "Weather briefing retrieved",
            }
        except Exception as e:
            logger.error(f"Failed to get weather briefing: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Weather briefing failed",
            }


class AviationWorkflowOrchestrator:
    """
    High-level orchestrator for complex aviation workflows.
    Combines multiple adapters to perform end-to-end operations.
    """

    def __init__(self, driver: WebDriverProtocol, config: Config) -> None:
        self.driver = driver
        self.config = config
        self.login_adapter = AviationLoginAdapter(driver, config)
        self.flight_plan_adapter = FlightPlanAdapter(driver, config)
        self.tankering_adapter = TankeringAdapter(driver, config)
        self.weather_adapter = WeatherAdapter(driver, config)

    def complete_flight_planning_workflow(
        self,
        user_credentials: UserCredentials,
        flight_data: FlightPlanData,
        include_weather: bool = True,
        include_tankering: bool = False,
    ) -> dict[str, Any]:
        """
        Complete end-to-end flight planning workflow.

        Args:
            user_credentials: User credentials for login
            flight_data: Flight plan data
            include_weather: Whether to include weather briefing
            include_tankering: Whether to include tankering calculations

        Returns:
            Dictionary with workflow results
        """
        logger.info("Starting complete flight planning workflow")

        workflow_results = {"success": True, "steps_completed": [], "errors": []}

        try:
            # Step 1: Login
            login_result = self.login_adapter.login_with_credentials(user_credentials)
            if login_result is None:
                raise Exception("Login failed")
            workflow_results["steps_completed"].append("login")

            # Step 2: Create flight plan
            fp_result = self.flight_plan_adapter.create_flight_plan(flight_data)
            if not fp_result["success"]:
                raise Exception(f"Flight plan creation failed: {fp_result['error']}")
            workflow_results["steps_completed"].append("flight_plan_creation")
            workflow_results["flight_plan_id"] = fp_result["flight_plan_id"]

            # Step 3: Weather briefing (optional)
            if include_weather:
                airports = [flight_data.departure, flight_data.arrival]
                if flight_data.alternate_1:
                    airports.append(flight_data.alternate_1)
                if flight_data.alternate_2:
                    airports.append(flight_data.alternate_2)

                weather_result = self.weather_adapter.get_weather_briefing(airports)
                if weather_result["success"]:
                    workflow_results["steps_completed"].append("weather_briefing")
                    workflow_results["weather_data"] = weather_result["weather_data"]
                else:
                    workflow_results["errors"].append(
                        f"Weather briefing failed: {weather_result['error']}"
                    )

            # Step 4: Tankering calculations (optional)
            if include_tankering:
                fuel_prices = {flight_data.departure: 5.50, flight_data.arrival: 6.25}
                tankering_result = self.tankering_adapter.calculate_tankering(
                    flight_data, fuel_prices
                )
                if tankering_result["success"]:
                    workflow_results["steps_completed"].append("tankering_calculation")
                    workflow_results["tankering_data"] = tankering_result
                else:
                    workflow_results["errors"].append(
                        f"Tankering calculation failed: {tankering_result['error']}"
                    )

            # Step 5: File flight plan
            file_result = self.flight_plan_adapter.file_flight_plan(
                fp_result["flight_plan_id"]
            )
            if file_result["success"]:
                workflow_results["steps_completed"].append("flight_plan_filing")
                workflow_results["filed_time"] = file_result["filed_time"]
            else:
                workflow_results["errors"].append(
                    f"Flight plan filing failed: {file_result['error']}"
                )

            logger.info(
                "Workflow completed successfully. "
                f"Steps: {workflow_results['steps_completed']}"
            )
            return workflow_results

        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            workflow_results["success"] = False
            workflow_results["errors"].append(str(e))
            return workflow_results
