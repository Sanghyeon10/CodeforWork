import pandas as pd
import datetime
import re


df= pd.read_excel(r'C:\Users\user\Desktop\아침수거.xls')
df = df[['수거/배달','고객명','요청일자']]
df['고객명'] = df['고객명'].apply(lambda x: x.split(' ')[-1])
df['날짜'] = df['요청일자'].apply(lambda x: x.split('\n')[0])
df['날짜'] = df['날짜'].apply(lambda x: datetime.datetime.strptime(x, '%y-%m-%d'))
df['요청일자'] = df['요청일자'].apply(lambda x: x.split('\n')[-1]).apply(lambda x: x[1:6])
df['시'] = df['요청일자'].apply(lambda x:x.split(':')[0])
df['분'] = df['요청일자'].apply(lambda x:x.split(':')[1])


print(df.loc[df.index[0],'날짜'])
name = input('몇동?')

for i in range(len(df)):
    if df.loc[df.index[i],'고객명']== name and int(df.loc[df.index[i],'시'])<=12 and (df.loc[df.index[i],'날짜']).weekday()!=5 and df.loc[df.index[i],'분']!='10': #12시전이 오전 ,5라면 토요일
        print(df.loc[df.index[i],'고객명'], df.loc[df.index[i],'날짜'], )