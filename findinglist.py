import pandas as pd
import os
import re
import datetime
from openpyxl import load_workbook
import making


def Save_file(new_row):
    file = "log.xlsx"
    # new_row = {
    #     "날짜": "2024-01-10",
    #     "내용": "보관 요청 발생",
    #     "수신번호": "010-1234-5678"
    # }

    # 파일이 이미 존재하면 → 기존 내용 불러오기 + append
    if os.path.exists(file):
        # print('test')
        df = pd.read_excel(file)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # 파일이 없으면 → 새로 생성
        df = pd.DataFrame([new_row])

    df.to_excel(file, index=False)

def has_recent_three(dates):
    # 날짜 정렬
    dates = sorted(dates)

    # 연속된 3개의 날짜가 30일 이내인지 확인
    for i in range(len(dates) - 2):
        # i번째 날짜와 i+2번째 날짜 비교
        if dates[i + 2] - dates[i] <= datetime.timedelta(days=30):
            return True

    return False

def getName(phonenumber,df1,df3):
    for i in range(len(df1.index)):
        for j in range(len(df3.index)):
            if len({phonenumber,
                    df1.loc[df1.index[i], '수신번호'],
                    df3.loc[df3.index[j], '전화번호']}) == 1:# 번호가 일치하면
                return df3.loc[df3.index[j], '이름']
    return None



# 행과 열 제한 해제
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)



df1, df2, df3 = making.Makedf()




# print(df1)

# 1) 문자내용에 '보관'이 포함된 행 필터링
filtered = df1[df1['문자내용'].str.contains('보관', na=False)]

# 2) 수신번호별로 전송일자 리스트로 정리
result = (
    filtered
    .assign(전송일자=pd.to_datetime(filtered['전송일자']))
    .sort_values('전송일자')
    .groupby('수신번호')['전송일자']
    .apply(list)
    .reset_index()
)

print(result)

for i in range(len(result.index)):
    # 보관재촉 문자 조건달성?.
    if has_recent_three(result.loc[result.index[i],'전송일자']):
        new_row = {
            "날짜": datetime.datetime.now().strftime("%Y-%m-%d"),
            "수신번호": result.loc[result.index[i],'수신번호'],
            "이름":getName(result.loc[result.index[i],'수신번호'],df1,df3 )
        }

        Save_file(new_row)
        print( new_row,"새로운 정보 기록")
    else:
        pass

