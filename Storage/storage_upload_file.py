#### upload files to googole cloud Storage

from google.cloud import storage

### set #####
# confirm the buckit name on Storage
bucket_name = 'project-187007.appspot.com' 
destination_blob_name = 'test/pic.jpg' # location of file on Storage
source_file_name = '/Users/apple/nicole/pic0.jpg' # lacal file
#############

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

# 上傳一個全新的blob
uploadBlob = bucket.blob(destination_blob_name)
uploadBlob.upload_from_filename(source_file_name)

print('File uploaded')
