import pandas as pd


df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob', 'Charlie'],
                   'Item': ['Apple', 'Orange', 'Banana', 'Apple', 'Banana', 'Apple']})

df2=pd.DataFrame()
# 특정 물품들의 개수 확인
item_counts = df.groupby('Name')['Item'].count()
print(item_counts)
df['Item'] = df['Item'].apply(lambda x: x if x in ('Apple') else None)
item_counts = df.groupby('Name')['Item'].count()
print(item_counts)

item_count= df2.groupby('고객명')['상품명'].count()
df2['고객명'] = df2['고객명'].apply(lambda x: x if x in ('운동화') else None)
shoe_count= df2.groupby('고객명')['상품명'].count()


for p in range(len(df2)):  # 옷장에 있는거 택번호 가져올 정보
    if df2.loc[df2.index[p], '고객명'] == globals()['get' + str(l)][i][0][1]:  # 맞는 택번호 구하기
        tagnumber = df2.loc[df2.index[p], '택번호']

        tempnumber= str(item_count['고객명']) + '운동화는'+ str(shoe_count)
        break  # 맞나?

#요긴 삭제
# for h in range(len(df3)):  # 개수 가져오기
#     if df3.loc[df3.index[h], '고객명'] == globals()['get' + str(l)][i][0][1]:
#         tempnumber = str(df3.loc[df3.index[h], '체류'])

# item_counts = df2.groupby('고객명')['상품명'].count()['고객명'] #완성한 개수
# shoes_counts = df2.groupby('고객명')['상품명'].apply(lambda x: sum(item in x for item in items)).reset_index(name='Count')



#import pandas as pd

# 샘플 데이터프레임 생성
# df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob'],
#                    'Age': [25, 30, 35, 27, 32],
#                    'City': ['New York', 'Paris', 'London', 'Paris', 'London'],
#                    'Salary': [50000, 60000, 70000, 55000, 65000]})
#
# # Name 열을 기준으로 그룹화
# grouped = df.groupby('Name')
#
# # 그룹화된 결과 출력
# for name, group in grouped:
#     print(f"Group: {name}")
#     print(group)
#     print()