### update information to firebase database: put
### author: Nicole
### 要一次新建時建議輸出為json檔在網頁上傳，更新使用put為佳

from firebase import firebase
import pandas as pd

# 連結到對應firebase database，須將rule改寫成 read,write: true
fbase = firebase.FirebaseApplication('https://evaair-tour-2018-winter.firebaseio.com', None)

detail = pd.read_excel('firebase/sample_detail.xlsx')
keyword = pd.read_excel('firebase/sample_keyword.xlsx')

i=0 ; Update_Result = dict()
airport = {'departure' : detail.loc[i, 'departure_airport'], 'landing' : detail.loc[i, 'landing_airport']}
airport = {'airport': airport}
dpio = {'dpio' : detail.loc[i, 'departure_airport'] == detail.loc[i, 'landing_airport']}

contries = ['法國', '瑞士', '盧森堡', '義大利', '英國', '荷蘭', '葡萄牙', '西班牙']
contries_value = [item in detail.loc[i, 'contry'].split('_') for item in contries]
contries = {'contries' : dict(zip(contries, contries_value))}

days = {'days' : str(detail.loc[i,'days1'])}
price = {'price' : str(detail.loc[i, 'price'])}
title = {'title' : detail.loc[i, 'title']}
Type = {'type': detail.loc[i, 'type']}

Update_Result = {**airport, **contries, **dpio, **days, **price, **title, **Type}
print(Update_Result)

## 更新資料，若key相同則會取代
fbase.put('tours', 'tourtest00', Update_Result)

## 也可以指更新其中一個值
fbase.put('tours/tourtest00', 'days', 100)

## post 會沒有key值
#fbase.post('test', Update_Result)
