"""
Manufacturing domain constants - tab names, user types, and domain-specific values.
"""

# User types for manufacturing domain
USER_PLANNER, USER_MANAGER, USER_COORDINATOR, USER_PARTNER = 0, 1, 2, 4

# Production Planning tabs (mapped from Flight Planning)
PRODUCTION_PLANNING = "Production Planning"  # Main tab
CREATE_ORDER = "Create Order"
ORDER_STATUS = "Order Status"
PRODUCTION_ROUTES = "Production Routes"
PRODUCTION_ROUTES_ALT = "Routes to Alt Production"
PRODUCTION_SLOT_STATUS = "Production Slots"
PRODUCTION_FAX_EMAIL_PKG = "Fax/Email Pkg"
PRODUCTION_PKG_STATUS = "Pkg Status"
PRODUCTION_QUICK_FILE = "Quick File"
PRODUCTION_GRAPHICAL_TFRS = "Graphical Production Flow"
PRODUCTION_RUNWAY_ANALYSIS = "Line Analysis"
PRODUCTION_RUNWAY_RESULTS = "Line Analysis Results"

# Quality Control tabs (mapped from Weather)
QC_QUALITY = "Quality Control"  # Main tab
QC_TEXT = "Text Quality Reports"
QC_BRIEFING2 = "Quality Briefing"
QC_GRAPHICAL = "Graphical Quality Control"
QC_BRIEFING = "Quality Control Briefing"
QC_CUSTOMER = "Customer Quality Reports"
QC_FACTORY = "Factory Quality Monitor"

# Safety tabs (mapped from Safety)
SAFETY_SAFETY = "Safety"  # Main tab
SAFETY_RISK_TEMPLATES = "Risk Assessment Templates"
SAFETY_TEMPLATE_ASSIGN = "Template Assignment"
SAFETY_RISK = "Risk Assessment"
SAFETY_SMS_DOCUMENTS = "Safety Management Documents"
SAFETY_PRODUCTION_RISK = "ProductionRisk® Analysis"
SAFETY_PRODUCTION_RISK1 = "ProductionRisk"
SAFETY_PRODUCTION_RISK2 = " Analysis"
SAFETY_VECTOR_SMS = "Vector SMS"

# Communication tabs (mapped from Messaging)
COMM_COMMUNICATION = "Communication"  # Main tab
COMM_COMPOSE = "Compose"
COMM_MESSAGE_CENTER = "Message Center"
COMM_VIEW_PAST_ORDERS = "View Past Orders"

# Factory Services (mapped from Cabin Services)
FACTORY_SERVICES = "Factory Services"
FACTORY_NETWORK_LOGON = "Network Logon"
FACTORY_NETWORK_CALLS = "Network Voice Calls"
FACTORY_SWIFT_64 = "Swift 64"
FACTORY_SWIFT_BROADBAND = "SwiftBroadband"

# Shipping tabs (mapped from APIS)
SHIPPING_SHIPPING = "Shipping"  # Main tab
SHIPPING_CREATE = "Create Shipping Manifest"
SHIPPING_STATUS = "Shipping Status"
SHIPPING_CUSTOMERS = "Manage Customers"

# My Account tabs
ACCT_MY_ACCOUNT = "My Account"  # Main tab
ACCT_USER = "User Profile"
ACCT_QC_PREF = "Quality Control Preferences"
ACCT_PRODUCTION_PREF = "Production Preferences"
ACCT_SITE_PREF = "Site Preferences"
ACCT_PKG_PREF = "Package Preferences"

# My Factory tabs (mapped from My Company)
FACTORY_MY_FACTORY = "My Factory"  # Main tab
FACTORY_USERS = "Users"
FACTORY_LINES = "Production Lines"
FACTORY_AFC = "Auto Forward Codes"
FACTORY_ORDER_IDS = "Order ID Assignments"
FACTORY_EXTERNAL_LINE = "External Factory Line Access"
FACTORY_LINE_PERMISSIONS = "Line Permissions"
FACTORY_PREF = "Factory Preferences"

# Materials tabs (mapped from Fuel)
MATERIALS_MAIN = "Materials"  # Main tab
MATERIALS_ORDER = "Order Materials"
MATERIALS_RELEASES = "Material Releases"
# Materials Admin tabs
MATERIALS_ADMIN = "Materials Admin"
MATERIALS_PRICES = "Material Prices"
MATERIALS_SHEETS = "Material Sheets"

# Documents
DOC_DOCUMENTS = "Documents"
DOC_TABLET = "Tablet"

# Alerts
ALERTS = "Alerts"  # Main Tab
MANAGE_ALERTS = "Manage Alerts"

# PC Queue tabs (mapped from FC Queue)
PC_QUEUE = "PC Queue"
PC_FF_QUEUE = "FF Queue"
PC_HANDLING = "PC Handling"
PC_TASKS = "PC Tasks"
PC_ARCHIVE = "Archive"
PC_MY_ARCHIVE = "My Archive"

# PC Info tabs (mapped from FC Info)
PC_INFO = "PC Info"  # Main tab
PC_USER_INFO = "User info"
PC_MONITOR = "Monitor"
PC_FLOW_CONTROL = "Flow Control"
PC_EAST_SUPPLY = "East Supply Chain"
PC_WEST_SUPPLY = "West Supply Chain"
PC_CONTACT = "Customer Contact Info"
PC_GRAPHIC_FLOW = "Graphical Production Flow"

# PC Admin tabs (mapped from FC Admin)
PC_ADMIN = "PC Admin"
PC_ALT_ROUTES = "Routes to Alt Production"
PC_PDC_LINES = "PDC Production Lines"
PC_AUTOFORWARD = "Auto Forward Codes"

# Production Slot Reservations tabs (mapped from Slot Reservations)
SLOT_RESERVATIONS = "Production Slot Reservations"
SLOT_STATUS = "Production Slot Status"
SLOT_ARO = "ARO Availability"
SLOT_IMPROVE = "Improve Slots"

# Customer Management tabs
PC_CUSTOMER_MANAGEMENT = "Customer Management"

# Super PC tabs (mapped from Super FC)
SUPER_MAIN = "Super PC"
SUPER_ORDER_ADMIN = "Production Order Admin"
SUPER_ROUTE_FIX = "Domestic Route Fix"
SUPER_LINE_SHARING = "Line Sharing"
SUPER_XML_LOOKUP = "XML Lookup"
SUPER_XML_RUNNER = "XML Runner"
SUPER_RHUMB = "Rhumb"
SUPER_PRODUCTION_RISK = "ProductionRisk Assessment Maintenance"

# Common
REFERENCE = "Reference"
TEST_CONSOLE = "TestConsole"

# Default user credentials for different environments
DEV_USERS = [
    ("planner1", "planner1"),
    ("manager1", "manager1"),
    ("coordinator1", "coordinator1"),
]
FAT_USERS = [
    ("TestPlanner", "Manufacturing test.22"),
    ("TestManager", "Manufacturing test.22"),
    ("PCTestBot", "Manufacturing test.22"),
]

# Standard password for production users
PASSWORD_ALL = "Manufacturing test.22"

# Page titles for Manufacturing System
FMS_TITLES = ["FMS", "Manufacturing Manufacturing System"]

# Production line types (mapped from aircraft types)
PRODUCTION_LINE_TYPES = [
    "CNC-001",
    "CNC-002",
    "CNC-003",
    "ASSEMBLY-A",
    "ASSEMBLY-B",
    "ASSEMBLY-C",
    "FINISHING-1",
    "FINISHING-2",
    "PACKAGING-1",
    "PACKAGING-2",
]

# Factory codes (mapped from airport codes)
FACTORY_CODES = {
    "FAC01": "Main Factory",
    "FAC02": "Secondary Factory",
    "WAR01": "Primary Warehouse",
    "WAR02": "Secondary Warehouse",
    "SUP01": "Supplier Hub 1",
    "SUP02": "Supplier Hub 2",
}

# Material types
MATERIAL_TYPES = {
    "WOOD": "Wood Materials",
    "FABRIC": "Fabric Materials",
    "HARDWARE": "Hardware Components",
    "FINISH": "Finishing Materials",
    "PACKAGING": "Packaging Materials",
}

# Production order statuses
ORDER_STATUSES = [
    "DRAFT",
    "SUBMITTED",
    "APPROVED",
    "IN_PRODUCTION",
    "QUALITY_CHECK",
    "COMPLETED",
    "SHIPPED",
    "CANCELLED",
]

# Quality control alert types (mapped from weather alerts)
QC_ALERT_TYPES = [
    "MATERIAL_DEFECT",
    "PRODUCTION_DELAY",
    "QUALITY_ISSUE",
    "EQUIPMENT_FAILURE",
    "SUPPLY_SHORTAGE",
]
