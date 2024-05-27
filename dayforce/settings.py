"""dayforce api settings and constants"""

# https://www.dayforcehcm.com/api/CompanyName/V1/Departments/[XRefCode]
# https://www.dayforcehcm.com/api/CompanyName/V1/Positions
# https://www.dayforcehcm.com/api/CompanyName/V1/LaborMetricTypes
# https://www.dayforcehcm.com/Api/einc/V1/Employees


from dlt.common import pendulum

BASE_URL = "https://www.dayforcehcm.com/api/"
CLIENT_NAME = "einc"

START_DATE = pendulum.datetime(year=2000, month=1, day=1)

TOKEN_API_URL = "https://dfid.dayforcehcm.com/connect/token"

EMPLOYEE_ENDPOINT = "V1/Employees"
EMPLOYEE_BULK_ENDPOINT = "V1/EmployeeExportJobs"

CRM_OBJECT_ENDPOINTS = {
    "employees": EMPLOYEE_ENDPOINT,
    "employees_bulk": EMPLOYEE_BULK_ENDPOINT
}

EMPLOYEE_FILTERS = [
    "contextDate",
    "xRefCode",
    "expand"
    "contextDateRangeFrom"
]

EMPLOYEE_EXPANDERS = [
    "Addresses",
    "AuthorizationAssignments",
    "CANFederalTaxes",
    "CANStateTaxes",
    "CANTaxStatuses",
    "ClockDeviceGroups",
    "CompensationSummary",
    "Contacts",
    "Courses",
    "DirectDeposits",
    "DocumentManagementSecurityGroups",
    "EIRates",
    "EmployeeCertifications",
    "EmergencyContacts",
    "EmployeeManagers",
    "EmployeeProperties",
    "EmployeePayAdjustCodeGroups",
    "EmployeeWorkAssignmentManagers",
    "EmploymentAgreements",
    "EmploymentStatuses",
    "EmploymentTypes",
    "Ethnicities",
    "GlobalProperties",
    "GLSplits",
    "HealthWellnessDetails",
    "HighlyCompensatedEmployees",
    "HRIncidents",
    "LaborDefaults",
    "Locations",
    "MaritalStatuses",
    "OnboardingPolicies",
    "OrgUnitInfos",
    "PayGradeRates",
    "PerformanceRatings",
    "Roles",
    "Skills",
    "SSOAccounts",
    "TrainingPrograms",
    "UnionMemberships",
    "UserPayAdjustCodeGroups",
    "USFederalTaxes",
    "USStateTaxes",
    "USTaxStatuses",
    "WorkAssignments",
    "WorkContracts"
]

DEPARTMENTS_ENDPOINT = "V1/Departments"

PROPERTIES_LIST = {
    "employees": [],
    "department": []

}

ALL = ("ALL",)
NONE = ""
