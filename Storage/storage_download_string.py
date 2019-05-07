### 需先執行 export 認證

from google.cloud import storage

bucket_name = 'training-article'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blobs = bucket.list_blobs()

for blob in blobs:
    index = blob.name
    content = blob.download_as_string().decode("utf-8")
    quit()
