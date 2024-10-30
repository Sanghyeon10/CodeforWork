from datetime import datetime, timedelta


import pandas as pd

# 예제 데이터프레임 생성
data = {
    'date': ['2023-01-01', '2023-01-02', '2023-01-02', '2023-01-03',
             '2023-02-01', '2023-03-02', '2023-03-01', '2023-03-02'],
    'value': [10, 20, 15, 30, 40, 25, 35, 45]
}
df = pd.DataFrame(data)

# 날짜열을 datetime 형식으로 변환
df['date'] = pd.to_datetime(df['date'])

# 날짜별로 데이터프레임을 나누기
dfs_by_date = {date: group for date, group in df.groupby(df['date'].dt.date)}

# 각 날짜별 데이터프레임 확인
for date, df_date in dfs_by_date.items():
    print(f"Date: {date}")
    print(df_date)
    print()