"""
This is a module that provides a DLT source to retrieve data from multiple endpoints of Dayforce API. The retrieved data is returned as a tuple of Dlt resources, one for each endpoint.
"""

from typing import Any, Dict, Iterator, List, Literal, Sequence
from urllib.parse import quote

import dlt
from dlt.common import pendulum
from dlt.common.typing import TDataItems
from dlt.sources import DltResource

from .helpers import get_xref, get_access_token, create_export_job, get_export_job_data_url, get_exported_data
from .settings import (
    ALL,
    NONE,
    EMPLOYEE_ENDPOINT,
    EMPLOYEE_BULK_ENDPOINT,
    EMPLOYEE_FILTERS,
    EMPLOYEE_EXPANDERS,
    DEPARTMENTS_ENDPOINT,
    PROPERTIES_LIST,
    BASE_URL,
    CLIENT_NAME,
    CRM_OBJECT_ENDPOINTS
)


@dlt.source(name="dayforce")
def dayforce(
    user_name: str = dlt.secrets.value,
    password: str = dlt.secrets.value
) -> Sequence[DltResource]:

    access_token = helpers.get_access_token(user_name, password)

    @dlt.resource(name="employees")
    def employees(
        access_token: str = access_token,
        props: Sequence[str] = ALL,
        query_params: Sequence[str] = None,
        include_custom_props = False
    ) -> Iterator[TDataItems]:

        yield from crm_objects(
            "employees",
            access_token,
            query_params,
            include_custom_props
        )

    return employees


def generate_query_params(object_type):
    pass


def generate_endpoint_url(object_type, query_params=None):
    if query_params is None:
        return f"{BASE_URL}{CLIENT_NAME}/{CRM_OBJECT_ENDPOINTS[object_type]}"
    else:
        query_params = generate_query_params(object_type)
        return f"{BASE_URL}{CLIENT_NAME}/{CRM_OBJECT_ENDPOINTS[object_type]}?{query_params}"


def crm_objects(
    object_type: str,
    access_token: str = dlt.secrets.value,
    query_params: Sequence[str] = None,
    include_custom_props: bool = False,
) -> Iterator[TDataItems]:
    """Building blocks for CRM resources."""

    endpoint_url = generate_endpoint_url(object_type, query_params)

    if include_custom_props:
        custom_props = [prop for prop in PROPERTIES_LIST[object_type]]
        print(custom_props)

    # params = {"properties": props, "limit": 100}

    yield from fetch_data(object_type, access_token, endpoint_url)


def fetch_data(object_type, access_token, endpoint_url):

    if object_type == "employees":

        # xref_list = get_xref(access_token=access_token, api_url=endpoint_url)
        xref_list = get_xref(access_token=access_token, api_url='https://www.dayforcehcm.com/api/einc/v1/Employees?EmploymentStatusXRefCode=Terminated')
        print(xref_list)

        # yield create_export_job(xref_string=xref_list, token=access_token, expanders=EMPLOYEE_EXPANDERS, bulk_url=generate_endpoint_url(object_type + "_bulk"))
        job_url = create_export_job(xref_string=xref_list, token=access_token, expanders=EMPLOYEE_EXPANDERS, bulk_url=generate_endpoint_url(object_type + "_bulk"))
        yield from get_exported_data(get_export_job_data_url(job_url, access_token), access_token)
