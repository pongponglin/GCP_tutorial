### 需先執行 export 認證

from google.cloud import storage

bucket_name = 'training-article'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

destination_blob_name = '{0}.txt'.format("testfile")
string = "測試檔案:文字內容"
uploadBlob = bucket.blob(destination_blob_name)
uploadBlob.upload_from_string(string)
print("upload success")
