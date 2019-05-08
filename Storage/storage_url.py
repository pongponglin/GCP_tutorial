# 取得storge 檔案的連結網址
### practice
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from google.cloud import storage



storage_client = storage.Client()
buckets = list(storage_client.list_buckets())
#print(buckets)
bucket = storage_client.get_bucket('project-ai-187007.appspot.com')

blobs = bucket.list_blobs()

#for blob in blobs:
#    print(blob.name)


# Part1 : 連結到某一個 blob
Blob = bucket.get_blob('test/pic.jpg')
#Blob.upload_from_string('New!') ## 修改這個blob的文字


a = Blob.path
b = Blob.public_url
c = Blob.self_link
d = Blob.content_disposition
e = Blob.component_count

print(a)
print(b)
print(c)
print(d)
print(e)


google = 'https://storage.cloud.google.com/project-ai-187007.appspot.com/test/pic.jpg'
fire = 'https://firebasestorage.googleapis.com/v0/b/project-ai-187007.appspot.com/o/test%2Fpic.jpg?alt=media&token=390876bb-242d-4c51-bfcd-0d8dc826b56a'
stor = 'https://00e9e64bac499349885480adaf970142053e3be9e2d51d970a-apidata.googleusercontent.com/download/storage/v1/b/project-ai-187007.appspot.com/o/test%2Fpic.jpg?qk=AD5uMEs_2fqVfuRTl0spxat8mTvdfhlumKXhQ9DiBCazBFspvTci-4t-wqJoKAX9jd3rXMgW-HSCT-YClbbZCyqZtbzSHWGlJiBX7YVzvbXRAOek5hfdKswJgIDaX5138gabXcmE9OhdrMLWx9y-9G9XHy8V2d8eOnVU5GG00oTPNYxGGHgGu8VcaOgWESqsIwLnbqMGhK7jXwdPy4bO_dykhhPE_b6jplZMAG7imU5gnXxzA7Pj6DZ-5mB0qbI6_EaH-Ea4LCzE_D2Vm-IebLQDyI0GZn57CQbBzqT4lnAtzOweKCnabbc9z3IyztxoJwy8_-j97kipBwiBx_-A-bwLnBPHS6Xl3LF0t0mHbBRPAsbL2UJg8BsojDoqjbzSfO29Z075DDQs1AoCcDKVO8AejeRxVWwkjgI-LOKfsg4P9JB6NaVuZ57Kxs1E4jc6Yqx2rw0rtl21zOonZJkowjWXi7JO2W7W7voe8S7K6tuugfkwaVkE9zY9Y-x4rm-3vbKxucAGfgoLPWRv1r1ShmCP0iBHTs4iLTL9I9pqkmDCUkQ7JJH_69KXYS3AfwWHmVCsAhP6spQSBIphqE4Cntk8_B-XNAv1lZwithM8OJuMydXgZglZ8NgtVsf7BzZE_a0MNXU0DRh8Fids2uxKtsCxk8rdurx6ZfThmM0SXpzoPCkN1WsiLgeOgKkLxKEpW-LXkD2RRi86Z8-j6uZOorZ2AVG2qYSGWtlbX0oPAwpjL6mQEizqqmAO37Uu07RoMRzmC1HPFRRa'

col = ["description", "score"]
Result = pd.DataFrame(columns = col)
index = 0

data = {'img': stor}
a = requests.post('https://us-central1-project-ai-187007.cloudfunctions.net/api/vision/labelDetection', data = data)
focus = a.json()[0]['labelAnnotations']

for j in range(len(focus)):
    vision = focus[j]
    Result.loc[index] = [vision['description'], vision['score']]
    index += 1

print(Result)
