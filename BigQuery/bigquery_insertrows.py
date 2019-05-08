### creat table on Bigquery and insert rows to the table
### Author: Nicole

from google.cloud import bigquery
from google.cloud.bigquery import Dataset

project_id = "web"
dataset_name = "nicoledataset"
client = bigquery.Client(project= project_id)
dataset_ref = client.dataset(dataset_name)
table_ref = dataset_ref.table('inserttable')

#--------creat tables
schema = [
    bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
]
table = bigquery.Table(table_ref, schema=schema)
table = client.create_table(table)   # API request

#--------inster rows into table, table必須先存在
table_ref = dataset_ref.table('inserttable')
gettable = client.get_table(table_ref)

rows_to_insert = [
    (u'Phred Phlyntstone', 32),
    (u'Wylma Phlyntstone', 29),
]
client.insert_rows(gettable, rows_to_insert)
