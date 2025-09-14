"""
Aviation domain constants - tab names, user types, and other domain-specific values.
"""

# User types for aviation domain
USER_REG, USER_ADMIN, USER_FC, USER_PROD = 0, 1, 2, 4

# Flight Planning tabs
FPL_FLIGHT_PLANNING = "Flight Planning"  # Main tab
FPL_CREATE = "Create FPL"
FPL_FILING_STATUS = "Filing Status"
FPL_ROUTES = "Routes"
FPL_ROUTES_ALT = "Routes to Alt"
FPL_SLOT_STATUS = "Slot Status"
FPL_FAX_EMAIL_PKG = "Fax/Email Pkg"
FPL_PKG_STATUS = "Pkg Status"
FPL_QUICK_FILE = "Quick File"
FPL_GRAPHICAL_TFRS = "Graphical TFRs"
FPL_RUNWAY_ANALYSIS = "Runway Analysis"
FPL_RUNWAY_RESULTS = "Runway Analysis Results"

# Weather tabs
WX_WEATHER = "Weather"  # Main tab
WX_TEXT = "Text Weather"
WX_BRIEFING2 = "Briefing"  # it was beta, has no weather in title
WX_GRAPHICAL = "Graphical Weather"
WX_BRIEFING = "Weather Briefing"
WX_PASSENGER = "Passenger Weather"
WX_AIRPORT = "Airport Radar"

# Safety tabs
SAFETY_SAFETY = "Safety"  # Main tab
SAFETY_FRAT_TEMPLATES = "FRAT Templates"
SAFETY_TEMPLATE_ASSIGN = "Template Assignment"
SAFETY_FRAT = "FRAT"
SAFETY_SMS_DOCUMENTS = "SMS Documents"
SAFETY_FLIGHT_RISK = "FlightRisk\xc2\xae Analysis"
SAFETY_FLIGHT_RISK1 = "FlightRisk"
SAFETY_FLIGHT_RISK2 = " Analysis"
SAFETY_VECTOR_SMS = "Vector SMS"

# Messaging tabs
MSG_MESSAGING = "Messaging"  # Main tab
MSG_COMPOSE = "Compose"
MSG_MESSAGE_CENTER = "Message Center"
MSG_VIEW_PAST_FLIGHTS = "View Past Flights"

# Cabin Services
CABIN_SERVICES = "Cabin Services"
CABIN_SATELITE_LOGON = "Satellite Logon"
CABIN_SATELITE_VOICE = "Satellite Voice Calls"
CABIN_SWIFT_64 = "Swift 64"
CABIN_SWIFT_BROADBAND = "SwiftBroadband"

# APIS tabs
APIS_APIS = "APIS"  # Main tab
APIS_CREATE = "Create APIS Manifest"
APIS_STATUS = "APIS Status"
APIS_TRAVELERS = "Manage Travelers"

# My Account tabs
ACCT_MY_ACCOUNT = "My Account"  # Main tab
ACCT_USER = "User Profile"
ACCT_WX_PREF = "Weather Preferences"
ACCT_FPL_PREF = "Flight Plan Preferences"
ACCT_SITE_PREF = "Site Preferences"
ACCT_PKG_PREF = "Package Preferences"

# My Company tabs
COMP_MY_COMPANY = "My Company"  # Main tab
COMP_USERS = "Users"
COMP_TAILS = "Tails"
COMP_AFC = "Auto Forward Codes"
COMP_FLIGHT_IDS = "Flight ID Assignments"
COMP_EXTERNAL_TAIL = "External Company Tail Access"
COMP_TAIL_PERMISSIONS = "Tail Permissions"
COMP_PREF = "Company Preferences"

# Fuel tabs
FUEL_MAIN = "Fuel"  # Main tab
FUEL_ORDER = "Order Fuel"
FUEL_RELEASES = "Fuel Releases"
# Fuel Admin tabs
FUEL_ADMIN = "Fuel Admin"
FUEL_PRICES = "Fuel Prices"
FUEL_SHEETS = "Fuel Sheets"

# Documents
DOC_DOCUMENTS = "Documents"
DOC_IPAD = "iPad"

# Alerts
ALERTS = "Alerts"  # Main Tab
MANAGE_ALERTS = "Manage Alerts"

# FC Queue tabs
FC_QUEUE = "FC Queue"
FC_FF_QUEUE = "FF Queue"
FC_HANDLING = "Handling Queue"
FC_TASKS = "FC Tasks"
FC_ARCHIVE = "Archive"
FC_MY_ARCHIVE = "My Archive"

# FC Info tabs
FC_INFO = "FC Info"  # Main tab
FC_USER_INFO = "User info"
FC_MONITOR = "Monitor"
FC_FLOW_CONTROL = "Flow Control"
FC_EAST_NATS = "East NATs"
FC_WEST_NATS = "West NATs"
FC_CONTACT = "Customer Contact Info"
FC_GRAPHIC_TFRS = "Graphical TFRs"

# FC Admin tabs
FC_ADMIN = "FC Admin"
FC_ALT_ROUTES = "Routes to Alt"
FC_PDC_AIRCRAFT = "PDC Aircraft"
FC_AUTOFORWARD = "Auto Forward Codes"

# Slot Reservations tabs
SLOT_RESERVATIONS = "Slot Reservations"
SLOT_STATUS = "Slot Status"
SLOT_ARO = "ARO Availability"
SLOT_IMPROVE = "Improve Slots"

# Customer Management tabs
FC_CUSTOMER_MANAGEMENT = "Customer Management"

# Super FC tabs
SUPER_MAIN = "Super FC"
SUPER_FPL_ADMIN = "Flight Plan Admin"
SUPER_ROUTE_FIX = "Domestic Route Fix"
SUPER_TAIL_SHARING = "Tail Sharing"
SUPER_XML_LOOKUP = "XML Lookup"
SUPER_XML_RUNNER = "XML Runner"
SUPER_RHUMB = "Rhumb"
SUPER_FLIGHT_RISK = "FlightRisk Assessment Maintenance"

# Common
REFERENCE = "Reference"
TEST_CONSOLE = "TestConsole"

# Default user credentials for different environments
DEV_USERS = [("user1", "user1"), ("ca1", "ca1"), ("fc1", "fc1")]
SAT_USERS = [
    ("Testbot", "Chicken dinner.22"),
    ("Testadmin", "Chicken dinner.22"),
    ("FCtestbot", "Chicken dinner.22"),
]

# Standard password for production users
PASSWORD_ALL = "Chicken dinner.22"

# Page titles
ARINC_DIRECT_TITLES = ["ARINCDirect", "ARINC Direct"]
