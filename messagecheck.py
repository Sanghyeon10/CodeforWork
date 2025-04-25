import pandas as pd
import os
import re
import datetime


def format_phone_number(phone_number) -> str:
    # 전화번호를 문자열로 변환
    phone_number = str(phone_number)

    # 전화번호가 이미 포맷에 맞는지 확인
    if re.match(r"^\d{3}-\d{4}-\d{4}$", phone_number):
        return phone_number
    # 전화번호 길이와 유효성 확인
    elif len(phone_number) == 11 and phone_number.isdigit():
        # 전화번호 포맷 변환
        return f"{phone_number[:3]}-{phone_number[3:7]}-{phone_number[7:]}"
    else:
        print("올바른 11자리 전화번호를 입력하세요.")

df1 = pd.read_excel(r'C:\Users\WD\Downloads\data1.xlsx')
filepath1= r'C:\Users\WD\Downloads\data2.xlsx'
filepath2= r'C:\Users\WD\Downloads\data3.xlsx'
filepath3= r'C:\Users\WD\Downloads\data4.xlsx'
filepath4= r'C:\Users\WD\Downloads\data5.xlsx'

for path in [filepath1,filepath2,filepath3,filepath4 ]:
    if os.path.exists(path):
        df2= pd.read_excel(path)

        if "예약일자" in df2.columns:
            df2.rename(columns={'예약일자': '전송일자'}, inplace=True)

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
df3['전화번호']= df3['전화번호'].apply(format_phone_number)
print(df3)



for i in range(len(df3.index)):
    print(df3.loc[df3.index[i], '이름'])
    # print(df3.loc[df3.index[i], '전화번호'])
    for j in range((len(df1))):
        if df1.loc[df1.index[j],'수신번호']==df3.loc[df3.index[i],'전화번호']:
            if df1.loc[df1.index[j],'날짜차이']<= 5: #7일 이하는 보내면 안됌
                print('너무 짧아')
            print(str(df1.loc[df1.index[j],'전송일자'].month)+ "/"+str(df1.loc[df1.index[j],'전송일자'].day) ,df1.loc[df1.index[j],'날짜차이'] ,'Days'  )
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
print(namelist)
print(len(namelist))
print()

for name in namelist:
    for i in range(len(df3)):
        if df3.loc[df3.index[i], '이름'] == name:
            print(df3.loc[df3.index[i], '전화번호'])

# print('유영석 재촉은 8월말 넘겨서')