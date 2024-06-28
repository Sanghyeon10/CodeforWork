import pandas as pd
import os
import re
import datetime

df1 = pd.read_excel(r'C:\Users\WD\Downloads\ThisMonth.xlsx')
filepath= r'C:\Users\WD\Downloads\lastMonth.xlsx'
if os.path.exists(filepath):
    df2= pd.read_excel(filepath)

    df1 = pd.concat([df1, df2], axis=0, ignore_index=True)

df1 = df1.sort_values(by='전송일자', ascending=False)

df1 = df1[['수신번호', '전송일자', '문자내용', '결과']]
df1['전송일자'] = pd.to_datetime(df1['전송일자'])
df1['날짜차이'] = (datetime.datetime.now() - df1['전송일자']).dt.days
# df1['전송일자']= pd.to_datetime(df1['전송일자'])
df1['문자내용'] = df1['문자내용'].str.replace('\n', '', regex=True)
print(df1)


df3= pd.read_excel(r'C:\Users\WD\Downloads\겨울옷재촉리스트.xlsx')
df3 = df3.dropna()
df3 = df3.drop_duplicates(subset='전화번호')
print(df3)



for i in range(len(df3.index)):
    print(df3.loc[df3.index[i], '이름'])
    # print(df3.loc[df3.index[i], '전화번호'])
    for j in range((len(df1))):
        if df1.loc[df1.index[j],'수신번호']==df3.loc[df3.index[i],'전화번호']:
            print(df1.loc[df1.index[j],'전송일자'].month ,df1.loc[df1.index[j],'전송일자'].day ,df1.loc[df1.index[j],'날짜차이'] ,'Days'  )
            # print(df1.loc[df1.index[j],'날짜차이'] ,'Days')
            print(df1.loc[df1.index[j], '문자내용'])
            if  df1.loc[df1.index[j],'결과'] != '성공':
                print('전송실패!!')
            print()


    print()

namelist=[]
with open ('namelist.txt', 'r', encoding="utf-8" ) as f:
    for line in f:
        namelist = namelist+  [line for line in re.split(r'\s|,|\.', line) if line]


# namelist = pd.read_csv('namelist.txt' , delimiter='\t')
# print(namelist)

for name in namelist:
    for i in range(len(df3)):
        if df3.loc[df3.index[i], '이름'] == name:
            print(df3.loc[df3.index[i], '전화번호'])