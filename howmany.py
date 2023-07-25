import pandas as pd
import supportmain

df4 = pd.read_excel(r'C:\Users\user\Desktop\접수.xls')
df4 = df4.fillna(method='ffill')
df4['고객명'] = df4['고객명'].apply(lambda x: x.split('\n')[0])

df4 = df4[['고객명', '상품명', '택번호']]
df4 = df4.drop_duplicates(subset='택번호')

item_count = df4.groupby('고객명')['상품명'].count()

# print(item_count.keys())
df1= supportmain.getdf1() #배달수거


# print(df1)
for i in range(len(df1)):
    print(df1.loc[df1.index[i],"고객명"], item_count.get(df1.loc[df1.index[i],"고객명"],'없음'))


