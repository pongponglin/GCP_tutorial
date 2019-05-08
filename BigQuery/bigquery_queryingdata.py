### querying data from BigQuery
### Author: Nicole

from google.cloud import bigquery
from google.cloud.bigquery import Dataset

project_id = "web"
dataset_name = "testdataset"
client = bigquery.Client(project= project_id)
dataset_ref = client.dataset(dataset_name)
table_ref = dataset_ref.table('test_table10')

query = (
    'SELECT * '
    'FROM `testdataset.test_table10`'
    'WHERE mac = "d4:38:9c:6d:f5:01"')
query_job = client.query(query, location = "US") # Must match the destination dataset location.

df = query_job.to_dataframe()
print(df.shape)
print(df)
