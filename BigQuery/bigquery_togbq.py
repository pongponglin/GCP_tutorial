from google.cloud import bigquery
from pandas.io.gbq import *
import pandas as pd

project_id = "bot"
bigquery_table = "crawling.label_compare"
label_compare = pd.read_csv('traingLabel_comparison.csv',encoding = "utf-8")

to_gbq(label_compare, bigquery_table, project_id, if_exists='replace')
