### download information from firebase database
### author: Nicole

from firebase import firebase
import pandas as pd

# 連結到對應firebase database，須將rule改寫成 read,write: true
firebase = firebase.FirebaseApplication('https://evaair-tour-2018.firebaseio.com', None)

#topics = firebase.get('topics', None)
#print(topics)
col = ['hashtag', 'pic', 'description','score']
Result = pd.DataFrame(columns = col)

## get 取得資料
photo = firebase.get('photos', None)
tags = list(photo.keys())
index = 0
for i in range(2):
    tag = tags[i]
    photo_key = list(photo[tag].keys())
    for pic in photo_key:
        for j in range(len(photo[tag][pic]["labels"])):
            description = photo[tag][pic]["labels"][j]['description']
            score = photo[tag][pic]["labels"][j]['score']

            Result.loc[index] = [tag, pic, description,score]
            index += 1


from collections import Counter
print(Counter(Result['description'].tolist()))
