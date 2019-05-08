# coding=utf8
## Author : Nicole
## 將 pandas 用法記下來
import pandas as pd

df1 = pd.DataFrame({"c1":['a','a','c','d','e'],"c2":[1,2,3,4,5]})
df2 = pd.DataFrame({"c1":['a','b','c','d'],"c3":[6,7,8,9]})

print(list(set(df1["c1"])))

print(df1)
print(df2)

#### cbind #####
print("cbind")
df3 = pd.concat([df1, df2], axis=1)
print(df3)
print(df3.drop(["c1"], axis=1))

#### rbind #####
print("rbind")
df4 = df1.append(df2)
print(df4)
print(df4.shape)
print("nrow: "+ str(df4.shape[0]))
print("ncol: "+ str(df4.shape[1]))

#####
print(df4.c2[df4.c1=='a'])

w = [1,3,4,6]
# print(df4)
df = df4[df4.c2.isin(w)]
df = df.groupby("c1",as_index = False).sum()
print(df)

#####
mergepd = pd.merge(df1, df2 , on="c1", how='inner')
mergepd["new"] = mergepd["c2"]/mergepd["c3"]*100
print(mergepd)
