import pandas as pd

# 집합 생성 (오늘 독촉할 사람들의 명단)
name_set = {'Alice',  'Charlie', 'David'}

# 미수금과 명단 데이터프레임 생성
df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie', 'David'],
                   'OutstandingAmount': [500, 1000, 300, 700]})

# 집합에 있는 사람들 중 미수금이 큰 순서대로 필터링 및 정렬
filtered_df = df[df['Name'].isin(name_set)].sort_values(by='OutstandingAmount', ascending=False)

# 독촉할 사람들의 명부 출력
contact_list = filtered_df['Name'].tolist()
for name in contact_list:
    print(name)
