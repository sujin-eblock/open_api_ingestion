import dlt
from airflow.decorators import dag
from dlt.common import pendulum
from dlt.helpers.airflow_helper import PipelineTasksGroup
import os

DAG_ID = os.path.basename(__file__).replace(".py", "")

# Modify the dag arguments
default_task_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': 'test@test.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,

}

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_task_args,
    dag_id=DAG_ID,
)
def load_data():
    # Set `use_data_folder` to True to store temporary data on the `data` bucket.
    # Use only when it does not fit on the local storage
    tasks = PipelineTasksGroup("pipeline_name", use_data_folder=False, wipe_local_data=True)

    # Import your source from pipeline script
    from hubspot import hubspot

    # Modify the pipeline parameters
    pipeline = dlt.pipeline(
        pipeline_name="hubspot",
        dataset_name="hubspot_dataset",
        destination="duckdb",
    )

    # Run the pipeline with the HubSpot source connector
    # Create the source, the "serialize" decompose option
    # will convert dlt resources into Airflow tasks.
    # Use "none" to disable it.
    tasks.add_run(
        pipeline,
        hubspot(),
        decompose="serialize",
        trigger_rule="all_done",
        retries=0,
        provide_context=True
    )

    # The "parallel" decompose option will convert dlt
    # resources into parallel Airflow tasks, except the
    # first one, which will be executed before any other tasks.
    # All the tasks will be executed in the same pipeline state.
    # tasks.add_run(
    #   pipeline,
    #   source(),
    #   decompose="parallel",
    #   trigger_rule="all_done",
    #   retries=0,
    #   provide_context=True
    # )

    # The "parallel-isolated" decompose option will convert dlt
    # resources into parallel Airflow tasks, except the
    # first one, which will be executed before any other tasks.
    # In this mode, all the tasks will use separate pipeline states.
    # tasks.add_run(
    #   pipeline,
    #   source(),
    #   decompose="parallel-isolated",
    #   trigger_rule="all_done",
    #   retries=0,
    #   provide_context=True
    # )

load_data()