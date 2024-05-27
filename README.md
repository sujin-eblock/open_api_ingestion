# Custom Data Ingestion

## Project Description

In this hackathon, I explored an alternative data ingestion strategy by developing a custom script to complement or replace our existing Fivetran setup. While Fivetran offers robust and automated data pipelines, this solution provides greater flexibility and control over the ingestion process, allowing us to tailor the data flow according to specific project requirements.

## Key Features
- **Custom Data Ingestion**: The solution is designed to handle various data sources, providing the ability to implement bespoke transformations and integrations that may not be fully supported by Fivetran. Eg dayforce
- **Enhanced Flexibility**: By writing our own code, we gained the ability to manage complex data logic and edge cases directly within the ingestion process.
- **Cost Efficiency**: Utilizing a custom script can potentially reduce costs associated with third-party ingestion services, especially for niche or low-volume data sources.
- **Schema Management**: This solution offers automatic schema management with schema evolution for complex API data
- **Data Transformation**: Automatic data transformation and integration with DBT, an already existing technology we use with in our org

## Technologies Used
- **Dlt Hub**: Python utility for schema management and data transformation https://dlthub.com/.
- **DuckDB**: Used for efficient, in-memory data handling within the script .
- **MWAA Airflow**: A local version of publicly available Amazon managed airflow instance https://github.com/aws/aws-mwaa-local-runner

This approach allowed us to experiment with custom solutions while assessing the trade-offs between managed services and bespoke development. The insights gained from this hackathon can guide future decisions on optimizing our data pipeline architecture.