"""Hubspot source settings and constants"""

from dlt.common import pendulum

STARTDATE = pendulum.datetime(year=2000, month=1, day=1)

CRM_CONTACTS_ENDPOINT = (
    "/crm/v3/objects/contacts?associations=companies"
)
CRM_COMPANIES_ENDPOINT = (
    "/crm/v3/objects/companies?associations=p_auction"
)
CRM_AUCTION_ENDPOINT = "/crm/v3/schemas/p_auction"
CRM_METRIC_ENDPOINT = "/crm/v3/schemas/p_metric"
CRM_PURCHASE_ENDPOINT = "/crm/v3/schemas/p_purchase"
CRM_SALE_ENDPOINT = "/crm/v3/schemas/p_sale"

CRM_OBJECT_ENDPOINTS = {
    "contact": CRM_CONTACTS_ENDPOINT,
    "company": CRM_COMPANIES_ENDPOINT,
    "p_auction": CRM_AUCTION_ENDPOINT,
    "p_metric": CRM_METRIC_ENDPOINT,
    "p_purchase": CRM_PURCHASE_ENDPOINT,
    "p_sale": CRM_SALE_ENDPOINT,
}

WEB_ANALYTICS_EVENTS_ENDPOINT = "/events/v3/events?objectType={objectType}&objectId={objectId}&occurredAfter={occurredAfter}&occurredBefore={occurredBefore}&sort=-occurredAt"

OBJECT_TYPE_SINGULAR = {
    "companies": "company",
    "contacts": "contact",
    "p_metric": "p_metric",
    "p_purchase": "p_purchase",
    "p_sale": "p_sale",
    "p_auction": "p_auction",
}

OBJECT_TYPE_PLURAL = {v: k for k, v in OBJECT_TYPE_SINGULAR.items()}

DEFAULT_COMPANY_PROPS = [
    "createdate",
    "domain",
    "hs_lastmodifieddate",
    "hs_object_id",
    "name",
]

DEFAULT_CONTACT_PROPS = [
    "createdate",
    "email",
    "firstname",
    "hs_object_id",
    "lastmodifieddate",
    "lastname",
]

DEFAULT_AUCTION_PROPS = [
    "hs_object_id"
]

DEFAULT_PURCHASE_PROPS = [
    "hs_lastmodifieddate",
    "hs_object_id"
]

DEFAULT_SALES_PROPS = [
    "hs_lastmodifieddate",
    "hs_object_id"
]

DEFAULT_METRICS_PROPS = [
    "hs_lastmodifieddate",
    "hs_object_id"
]

ALL = ("ALL",)
