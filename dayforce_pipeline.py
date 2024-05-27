from typing import List
import dlt

from dayforce import dayforce


def load_crm_data() -> None:
    """
    This function loads all resources from Dayforce CRM

    Returns:
        None
    """

    # Create a DLT pipeline object with the pipeline name, dataset name, and destination database type
    # Add full_refresh=(True or False) if you need your pipeline to create the dataset in your destination
    p = dlt.pipeline(
        pipeline_name="dayforce",
        dataset_name="dayforce_dataset",
        destination="duckdb",
    )

    # Run the pipeline with the HubSpot source connector
    info = p.run(dayforce())

    # Print information about the pipeline run
    print(info)


if __name__ == "__main__":
    # Call the functions to load HubSpot data into the database with and without company events enabled
    load_crm_data()
    # load_crm_data_with_history()
    # load_web_analytics_events("company", ["7086461639", "7086464459"])
    # load_crm_objects_with_custom_properties()
