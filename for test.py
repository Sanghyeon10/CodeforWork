import pandas as pd

# 데이터프레임 생성
data = {'Column1': ['바지', '바지', '바지', '바지', '셔츠', '셔츠']}
df = pd.DataFrame(data)

# '바지' 값에 번호 붙이기
df['Column1'] = df['Column1'].where(
    df['Column1'] != '바지',
    df.groupby('Column1').cumcount().add(1).map(lambda x: f"바지{x}")
)

print(df)

