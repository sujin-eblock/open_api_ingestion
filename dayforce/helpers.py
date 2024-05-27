import json
import requests
import time
from datetime import datetime
from .settings import (
    TOKEN_API_URL,
    CLIENT_NAME
)

def validate_response(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Exception: {str(response.status_code)}. Message:{err}")


def get_access_token(user_name, password):
    payload = {
        "grant_type": "password",
        "companyId": CLIENT_NAME,
        "username": user_name,
        "password": password,
        "client_id": "Dayforce.HCMAnywhere.Client"
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.request("POST", TOKEN_API_URL, data=payload, headers=headers)
    except requests.exceptions.RequestException as err:
        raise Exception(err)

    response.encoding = 'utf-8'
    response_json = response.json()

    validate_response(response)
    return response_json["access_token"]


# def create_export_job(xref_string, token, bulk_url, expanders):
#     """
#         Get API calls for data ingestion
#
#         Parameters
#         ----------
#         expanders: additional columns to add based on documentation
#         xref_string: List of xrefs to pull as a single string comma separated
#         Returns
#         ----------
#         response: json response of API
#         """
#     payload = json.dumps({
#         "EmployeeXRefCode": xref_string,
#         "Expand": ",".join(expanders)
#     })
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {token}'
#     }
#     params = {
#         "isValidateOnly": "true"
#     }
#
#     response = requests.request("POST", url=get_redirected_url(bulk_url), headers=headers, data=payload, params=params)
#     response.encoding = 'utf-8'
#     response_json = response.json()['Data']['JobStatus']
#     # json_object = json.dumps(response_json)
#
#     while True:
#         status_response = requests.request("GET", response_json, headers=headers)
#         status = status_response.json()['Data']['Status']
#         if status == 'Received':
#             print(status + " as of : " + str(datetime.now()))
#         else:
#             if status != 'Succeeded':
#                 print("Beyond received but not there yet")
#                 print(status + " as of : " + str(datetime.now()))
#             else:
#                 print("Succeeded at : " + str(datetime.now()))
#                 file_url = status_response.json()['Data']['Results']
#                 break
#         time.sleep(5)
#
#     data = requests.request("GET", file_url, headers=headers)
#     json_out = data.json()['Data']
#     print("Initial Count of records")
#     print(len(json_out))
#     pagination = data.json()['Paging']['Next']
#     while True:
#         print(pagination)
#         if pagination.strip() != "":
#             print("Extract additional records")
#             pagination_request = requests.request("GET", pagination, headers=headers).json()
#             pagination_json = pagination_request['Data']
#             print("add additional " + str(len(pagination_json)) + "records")
#             print(type(pagination_json))
#             print(type(json_out))
#             json_out = json_out + pagination_json
#             print(str(json_out))
#         else:
#             print("no more pagination")
#             break
#         pagination = pagination_request['Paging']['Next']
#     yield json_out

def create_export_job(xref_string, token, bulk_url, expanders):
    """
        Get API calls for data ingestion

        Parameters
        ----------
        expanders: additional columns to add based on documentation
        xref_string: List of xrefs to pull as a single string comma separated
        Returns
        ----------
        response: json response of API
        """
    payload = json.dumps({
        "EmployeeXRefCode": xref_string,
        "Expand": ",".join(expanders)
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    params = {
        "isValidateOnly": "true"
    }

    response = requests.request("POST", url=get_redirected_url(bulk_url), headers=headers, data=payload, params=params)
    print(response.json()['Data']['Message'])
    job_url = response.json()['Data']['JobStatus']
    return job_url


def get_export_job_data_url(job_url, access_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    while True:
        status_response = requests.request("GET", job_url, headers=headers)
        job_status = status_response.json()['Data']['Status']
        print(job_status)
        if job_status == 'Succeeded':
            export_file_url = status_response.json()['Data']['Results']
            break
        else:
            time.sleep(10)

    return export_file_url


def get_exported_data(export_file_url, access_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    records_count = 0
    json_out = []
    export_file_url = export_file_url
    while True:
        data = requests.request("GET", export_file_url, headers=headers)
        json_out += data.json()['Data']
        records_count += len(data.json()['Data'])
        print(records_count)
        if data.json()['Paging']['Next'] != "":
            export_file_url = data.json()['Paging']['Next']
        else:
            break
    yield json_out

def get_redirected_url(input_url):
    url_response = requests.get(url=input_url)
    return url_response.url


def get_xref(access_token, api_url):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = None
    try:
        response = requests.request("GET", url=get_redirected_url(api_url), headers=headers)
        validate_response(response)
    except requests.exceptions.RequestException as err:
        raise Exception(str(err))
    except Exception as e:
        print(f"An error occurred: {e}")
        raise SystemExit(e)

    if response.json()['Data'] is None:
        print("Xref Values not returned")
        xref_string_output = ""
    else:
        xref_string_output = str('"' + ','.join([data['XRefCode'] for data in response.json()['Data']]) + '"')

    # xref_list_out = []
    # for x in xref_list_raw:
    #     xref_list_out.append(x['XRefCode'])
    # xref_string_output = str('"' + ','.join(xref_list_out) + '"')
    return xref_string_output


if __name__ == "__main__":
    token = get_access_token(token_api_url='')

    xref_list = get_xref(access_token=token, api_url='https://www.dayforcehcm.com/api/einc/V1/Employees?EmploymentStatusXRefCode=Terminated')
    print(xref_list)

    job_id = create_export_job(xref_string=xref_list, token=token, expanders=expanders, bulk_url='https://www.dayforcehcm.com/Api/einc/V1/EmployeeExportJobs')
    # check_export_job_status(job_id)
    # print("success")

    # https://www.dayforcehcm.com/api/CompanyName/V1/Departments/[XRefCode]
    # https://www.dayforcehcm.com/api/CompanyName/V1/Positions
    # https://www.dayforcehcm.com/api/CompanyName/V1/LaborMetricTypes
    # https://www.dayforcehcm.com/Api/einc/V1/Employees
