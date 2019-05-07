### upload Bigquery table from a file
### Author: Nicole

from google.cloud import bigquery
from google.cloud.bigquery import Dataset
import pandas

project_id = "ixq-web"
dataset_name = "nicoledataset"
client = bigquery.Client(project= project_id)
dataset_ref = client.dataset(dataset_name)
table_ref = dataset_ref.table('dataframe')
records = [
    {'title': 'The Meaning of Life', 'release_year': 1983},
    {'title': 'Monty Python and the Holy Grail', 'release_year': 1975},
    {'title': 'Life of Brian', 'release_year': 1979},
    {
        'title': 'And Now for Something Completely Different',
        'release_year': 1971
    },
]
dataframe = pandas.DataFrame(records)
print(dataframe)

client.load_table_from_dataframe(dataframe, table_ref, location='US')
