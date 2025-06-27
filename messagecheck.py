import pandas as pd
import os
import re
import datetime


# 행과 열 제한 해제
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def format_phone_number(phone_number) -> str:
    phone_number = str(phone_number)
    if re.match(r"^\d{3}-\d{4}-\d{4}$", phone_number):
        return phone_number
    elif len(phone_number) == 11 and phone_number.isdigit():
        return f"{phone_number[:3]}-{phone_number[3:7]}-{phone_number[7:]}"
    else:
        print("올바른 11자리 전화번호를 입력하세요.")
        return phone_number


# 문자 발송 이력 데이터 불러오기 및 병합
df1 = pd.read_excel(r'C:\Users\WD\Downloads\data1.xlsx')
filepaths = [
    r'C:\Users\WD\Downloads\data2.xlsx',
    r'C:\Users\WD\Downloads\data3.xlsx',
    r'C:\Users\WD\Downloads\data4.xlsx',
    r'C:\Users\WD\Downloads\data5.xlsx'
]

for path in filepaths:
    if os.path.exists(path):
        df2 = pd.read_excel(path)
        if "예약일자" in df2.columns:
            df2.rename(columns={'예약일자': '전송일자'}, inplace=True)
        df1 = pd.concat([df1, df2], axis=0, ignore_index=True)

df1 = df1.sort_values(by='전송일자', ascending=False)
df1 = df1[['수신번호', '전송일자', '문자내용', '결과']]
df1['전송일자'] = pd.to_datetime(df1['전송일자'])
df1['날짜차이'] = (datetime.datetime.now() - df1['전송일자']).dt.days
df1['문자내용'] = df1['문자내용'].str.replace('\n', '', regex=True)

# 대상자 리스트 불러오기 및 전화번호 포맷 정리
df3 = pd.read_excel(r'C:\Users\WD\Downloads\겨울옷재촉리스트.xlsx')
df3 = df3.dropna()
df3 = df3.drop_duplicates(subset='전화번호')
df3['전화번호'] = df3['전화번호'].apply(format_phone_number)

# 문자 이력 확인
for i in range(len(df3.index)):
    print(df3.loc[df3.index[i], '이름'])
    for j in range(len(df1)):
        if df1.loc[df1.index[j], '수신번호'] == df3.loc[df3.index[i], '전화번호']:
            if df1.loc[df1.index[j], '날짜차이'] <= 5:
                print('너무 짧아')
            print(f"{df1.loc[df1.index[j], '전송일자'].month}/{df1.loc[df1.index[j], '전송일자'].day} "
                  f"{df1.loc[df1.index[j], '날짜차이']} Days")
            print(df1.loc[df1.index[j], '문자내용'])
            if df1.loc[df1.index[j], '결과'] != '성공':
                print('전송실패!!')
            print()
    print()

# 이름 리스트 로드
namelist = []
with open('namelist.txt', 'r', encoding="utf-8") as f:
    for line in f:
        namelist += [word for word in re.split(r'\s|,|\.', line) if word]

print(namelist)
print(len(namelist))
print()

# 최근 5일 이내 문자 수신자 목록 출력
recent_df = df1[df1['날짜차이'] >=0 ]
recent_numbers = recent_df['수신번호'].unique()


print("\n✅ 최근  문자 수신자 전화번호 + 날짜차이 목록:")
recent_number_diff = recent_df[['수신번호', '날짜차이']].drop_duplicates()
# print(recent_number_diff)
# 전화번호 기준으로 df3와 조인 (df3['전화번호']와 recent_number_diff['수신번호'])
recent_number_diff = recent_number_diff.merge(
    df3[['이름', '전화번호']],
    left_on='수신번호',
    right_on='전화번호',
    how='left'
)

# '전화번호' 컬럼은 중복이므로 제거
recent_number_diff.drop(columns='전화번호', inplace=True)
recent_number_diff = recent_number_diff.dropna()
# 결과 출력
# print(recent_number_diff)

recent_number_diff = recent_number_diff.drop_duplicates(subset='이름')
print(recent_number_diff)
print(len(recent_number_diff))




# namelist에 포함된 이름의 전화번호와 문자 발송 이력 출력
print("\n📋 namelist에 있는 이름들의 전화번호:")
namelist_phones = []

for name in namelist:
    for i in range(len(df3)):
        if df3.loc[df3.index[i], '이름'] == name:
            phone = df3.loc[df3.index[i], '전화번호']
            namelist_phones.append(phone)
            print(phone)

print("\n📋 namelist에 있는 이름들의 전화번호 + 날짜차이:")

for name in namelist:
    # df3에서 이름으로 검색
    matched = df3[df3['이름'] == name]

    if not matched.empty:
        phone = matched.iloc[0]['전화번호']
        # 문자 이력에서 해당 전화번호에 대한 이력 필터
        history = df1[df1['수신번호'] == phone]

        if not history.empty:
            recent = history.sort_values(by='전송일자', ascending=False).iloc[0]
            days_diff = recent['날짜차이']
            print(f" {name},  {phone},  {days_diff}")
        else:
            print(f"이름: {name}, 전화번호: {phone}, 날짜차이: 문자 발송 이력 없음")
    else:
        print(f"이름: {name}, 전화번호: 없음, 날짜차이: 정보 없음")


print('김현옥 공릉아파트 현충일 이후 문자')