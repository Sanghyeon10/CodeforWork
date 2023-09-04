import pandas as pd

# 데이터프레임 생성 (고객명, 접수일자, 완성일자, 물건번호 열을 포함한 예제)
data = {'고객명': ['고객1', '고객1', '고객1', '고객2', '고객2', '고객3'],
        '접수일자': ['2023-08-01', '2023-08-02', '2023-08-01', '2023-08-02', '2023-08-02', '2023-08-03'],
        '완성일자': ['2023-08-03', '2023-08-05', '2023-08-02', '2023-08-04', '2023-08-03', '2023-08-04'],
        '물건번호': [1, 2, 3, 4, 5, 6]}
df = pd.DataFrame(data)

# 날짜 열을 DateTime 형식으로 변환
df['접수일자'] = pd.to_datetime(df['접수일자'])
df['완성일자'] = pd.to_datetime(df['완성일자'])


# 고객별로 그룹화
customer_grouped = df.groupby('고객명')

# 각 고객별로 "접수일자"별로 다시 그룹화
result = customer_grouped.apply(lambda group: group.groupby('접수일자').apply(lambda sub_group: sub_group['완성일자'].max() - sub_group['완성일자'].min()))

# 결과 출력
# print(type(result))
# print(result)
# print(result.index)
ID='고객1'
print((result[ID]))

# 시리즈에서 인덱스 추출
index_values = result[ID].index
# 첫 번째와 마지막 인덱스 선택
first_index = index_values[0]
last_index = index_values[-1]
# 결과 출력
print("첫 번째 인덱스:", first_index)
print("마지막 인덱스:", last_index)
# 합까지 구하기 가능
# print(result['고객1'].loc['2023-08-01':'2023-08-02'])
data = result[ID].loc[first_index:last_index].values
# total_days = data.astype('timedelta64[D]').sum()
total_days = data.astype('timedelta64[D]').sum().astype(int)
print((total_days))
last_date = result.loc[ :(ID, last_index)].values
timedelta_value = result.loc[(ID, last_index)]
print("마지막 날짜:", type(timedelta_value))
# print( result.loc[('고객1', '2023-08-01'):('고객1', '2023-08-02')].values)