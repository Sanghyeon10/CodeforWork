import pandas as pd

# 데이터프레임 생성
df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob',"Bob"],
                   'Number': [10, 20, 15, 25, 30,45]})

# 'Name'을 기준으로 그룹화한 후, 'Number' 칼럼 값의 차이 구하기
grouped_df = df.groupby('Name')['Number'].diff()
print(type(grouped_df))
# 'Name'을 기준으로 그룹화한 후, 'Number' 칼럼 값의 차이의 누적합 구하기
cumulative_sum = grouped_df.groupby(df['Name']).cumsum()
print(cumulative_sum)
# 모든 사람의 마지막 값 출력
last_values = cumulative_sum.groupby(df['Name']).last()

print(last_values)