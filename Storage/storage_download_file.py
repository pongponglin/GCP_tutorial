### download files from googole cloud Storage

from google.cloud import storage

### set #####
bucket_name = 'project-ai-187007.appspot.com'
destination_blob_name = 'ig_picture/11024107_838713289520944_1923731223_n.jpg'
download_file_name = '/Users/apple/nicole/IXQ/IXQ_code/1223.jpg'
#############

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

blob = bucket.blob(destination_blob_name)
blob.download_to_filename(download_file_name)

print(blob)
