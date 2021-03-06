# GCP_tutorial
**python**

## Finish Certification first
https://console.cloud.google.com/apis/credentials

### 1.Service Account Key
Enable server-to-server, app-level authentication using robot account

- Create cerdentials -> `Service account key`
- choose`App Engine defalut service account`
連動到Bigquery必須有較強的 Service account
- create 後會下載一個json檔， ex:web-4e4a64c233ca.json
- 通過 google account 認證

#### 在程式碼裡裝上傳金鑰
- 將金鑰的json file放置在專案資料夾中
```
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/apple/Downloads/aiii-web-4e4a64c233ca.json'
```

-----

## API
- Nature language api
	- [Entities](https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity):文字內容的實體詞語與類別
	- [Sentiment](https://cloud.google.com/natural-language/docs/reference/rest/v1/Sentiment):詞語正負面分數分析

- NLPapi.py: Entities Analysis. Give context and return Dataframe with words, types, and salience columns.

## BigQuery
```ruby
from google.cloud import bigquery
from google.cloud.bigquery import Dataset
```

### querying data from BigQuery
```ruby
client = bigquery.Client(project= project_id)
dataset_ref = client.dataset(dataset_name)
table_ref = dataset_ref.table('test_table10')
query = (
    'SELECT * '
    'FROM `testdataset.test_table10`'
    'WHERE mac = "d4:38:9c:6d:f5:01"')
query_job = client.query(query, location = "US") # Must match the destination dataset location.
```

### input data to BigQuery
- **create a table on bq**
```ruby
client = bigquery.Client(project= project_id)
dataset_ref = client.dataset(dataset_name)
table_ref = dataset_ref.table('inserttable')
schema = [
    bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
]
table = bigquery.Table(table_ref, schema=schema)
table = client.create_table(table)   # API request
```

- **insert rows into table on bq**
```ruby
table_ref = dataset_ref.table('inserttable')
gettable = client.get_table(table_ref)

rows_to_insert = [
    (u'Phred Phlyntstone', 32),
    (u'Wylma Phlyntstone', 29),
]
client.insert_rows(gettable, rows_to_insert)
```

- **to_gbq**
```ruby
import pandas as pd
label_compare = pd.read_csv('traingLabel_comparison.csv',encoding = "utf-8")
to_gbq(label_compare, bigquery_table, project_id, if_exists='replace')
```

- **upload a local file to bq**
```ruby
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
```

## Storage
```ruby
from google.cloud import storage
```

### upload 
- confirm the buckit name on Storage
```ruby
bucket_name = 'project-187007.appspot.com' 
destination_blob_name = 'test/pic.jpg' # location of file on Storage
source_file_name = '/Users/apple/nicole/pic0.jpg' # lacal file
#### upload a local file #########
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
# 上傳一個全新的blob
uploadBlob = bucket.blob(destination_blob_name)
uploadBlob.upload_from_filename(source_file_name)

##### upload string as file ########
destination_blob_name = '{0}.txt'.format("testfile")
string = "測試檔案:文字內容"
uploadBlob = bucket.blob(destination_blob_name)
uploadBlob.upload_from_string(string)

```

### download
```ruby
bucket_name = 'project-ai-187007.appspot.com'
destination_blob_name = 'ig_picture/11024107_838713289520944_1923731223_n.jpg'
download_file_name = '/Users/apple/nicole/IXQ/IXQ_code/1223.jpg'
#############
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.download_to_filename(download_file_name)

```
