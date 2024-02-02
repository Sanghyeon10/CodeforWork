import re
import pandas as pd
import supportmain
import datetime
import matplotlib.pyplot as plt

df = pd.read_excel(r'C:\Users\user\Desktop\엑셀.xls')
df=df[["접수일자","고객명","접수금액","택번호"]]
df= df.fillna(method='ffill')
# df=df.drop_duplicates(subset='택번호') #수선등 사항도 날라감

df['접수금액'] = df['접수금액'].apply(lambda x: int(x.replace(",", "")))
df['고객명'] = df['고객명'].apply(lambda x: x.split('\n')[0])
df['비입주'] = df['고객명'].apply(lambda x: "ex" if supportmain.check_words_in_string(["해마루"], x) == True else 'in')

df['접수일자'] = df['접수일자'].apply(lambda x: x.split('\n')[0]).apply(lambda x: '20' + x)
df['접수일자'] = df['접수일자'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

# print(df.columns)
# print(df.head(30))

# 월별로 그룹화
df['연도'] = df['접수일자'].dt.year
df['월'] = df['접수일자'].dt.month
monthly_sales = df.groupby(["연도",'월', '비입주'])['접수금액'].sum().unstack(fill_value=0)/1000

print(monthly_sales)

monthly_sales.plot(kind="bar",rot=0)
plt.show()

# # 2022년 1월부터 2023년 11월까지의 연도와 월 조합 생성
# start_year = 2022
# end_year = 2023
# start_month = 1
# end_month = 11
#
# date_combinations = [(year, month) for year in range(start_year, end_year + 1) for month in range(start_month, end_month + 1)]
# multi_index = pd.MultiIndex.from_tuples(date_combinations, names=['연도', '월'])
# # 데이터프레임 생성
# yearly_monthly_sales = pd.DataFrame(monthly_sales, index=multi_index)
#
# # 그래프 크기 설정
# plt.figure(figsize=(10, 6))
#
# # 데이터프레임을 월별로 그래프 생성
# for month, df_month in yearly_monthly_sales.groupby(level='월'):
#     plt.bar(df_month.index.get_level_values('연도'), df_month['입주민'], label=f'입주민 - {month}월', alpha=0.7)
#     plt.bar(df_month.index.get_level_values('연도'), df_month['비입주'], label=f'비입주민 - {month}월', alpha=0.7)
#
# # 그래프 제목 및 레이블 설정
# plt.title('월별 입주민 vs. 비입주민 매출')
# plt.xlabel('연도')
# plt.ylabel('매출')
# plt.legend(loc='upper left')
#
# # x축 레이블 설정
# plt.xticks(yearly_monthly_sales.index.get_level_values('연도').unique())
#
# # 그래프 표시
# plt.show()






