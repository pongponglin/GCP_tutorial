### upload a local file to Bigquery table 
### Author: Nicole

from google.cloud import bigquery
from google.cloud.bigquery import Dataset
import pandas

project_id = "web"
dataset_name = "nicoledataset"
client = bigquery.Client(project= project_id)
dataset_ref = client.dataset(dataset_name)
table_ref = dataset_ref.table('sampletable')

schema = [
    bigquery.SchemaField('timestamp', 'TIMESTAMP', mode='NULLABLE'),
    bigquery.SchemaField('mac', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('vendor', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('ts', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('rssi', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('sn', 'INTEGER', mode='NULLABLE'),
]
table = bigquery.Table(table_ref, schema=schema)
table = client.create_table(table)   # API request

job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.autodetect = True

filename = "/Users/apple/nicole/sample.csv"
with open(filename, 'rb') as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location='US',  # Must match the destination dataset location.
        job_config=job_config)
