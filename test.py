import pandas as pd
import datetime
import re

def contains_korean(text):
    #한글자라도 한글이 있는가?
    return re.search("[가-힣]+",text) #맞으면 값이 있고 없으면 NONE

def makejungbok(listt,X):
    if X in listt: #값이 있다.
        return True#중복임

    else:
        listt.append(X)
        return False #값이 없으니까 중복아님



now = datetime.datetime.now() #+ datetime.timedelta(days=3)
print('오늘날짜',now)

inputt= input('비입주이면 a입력')
if inputt == "a":
    A='비입주민'
    day=5 # 월요일까지 뒤로 돌리고 여기서 5일 더 뒤로 돌려야 수요일됨

else:
    A='입주민'
    day=2 # 월요일에서 토요일로 2일뒤로

week = now.weekday()+day

df= pd.read_excel(r'C:\Users\user\Desktop\옷장조회.xls')

# print(df)
df= df[['접수일자','완성일자', '고객명','옷장번호']]
df =df.dropna()



df['접수일자']= df['접수일자'].apply(lambda x: x.split('\n')[0]).apply(lambda x: '20'+x)
df['완성일자']= df['완성일자'].apply(lambda x: x.split('\n')[0]).apply(lambda x: '20'+x)

df['고객명']= df['고객명'].apply(lambda x: x.split('\n')[0])

df['비입주']=df['고객명'].apply(lambda x: x.split('-')[0] if contains_korean(x) != None else '입주민')

df=df[df['옷장번호']==0]

#비입주 조절용
df=df[df['비입주']==A]



df['접수일자']= df['접수일자'].apply(lambda x: datetime.datetime.strptime(x , "%Y-%m-%d"))
df['완성일자']= df['완성일자'].apply(lambda x: datetime.datetime.strptime(x , "%Y-%m-%d"))
df['몇주째']= df['완성일자'].apply(lambda x: x.strftime("%U"))


df['날짜차이']= df['완성일자']-df['접수일자']

pastSat= now - datetime.timedelta(days= (week))

print(pastSat)


df=df[df['완성일자']<=pastSat]

# print(df)

#전화번호,전화여부 뽑기
dff= pd.read_excel(r'C:\Users\user\Desktop\고객정보.xls')

dff= dff[['고객명','휴대폰','체류','주소','특이사항']]

dff['고객명']= dff['고객명'].apply(lambda x: x.split('\n')[0])
dff.fillna('',inplace=True)
dff['전화여부'] = dff[['주소','특이사항']].apply(lambda x:'전화' in ''.join(x),axis=1)



####

#배달 리스트 가져오기
df2= pd.read_excel(r'C:\Users\user\Desktop\수거배달.xls')
df2 = df2[['수거/배달','고객명']]
df2['고객명'] = df2['고객명'].apply(lambda x: x.split(' ')[-1])

# print(df2)


numberlist=[]
remaining=0 #남아있는거 세는 변수
jungbokcheck=[]
BB=''
CC=''
gijun=df.loc[df.index[0],'몇주째']

# print(df)
for i in range(len(df)):
    # print(df.loc[dff.index[i],'고객명'],df.loc[df.index[i],'날짜차이'].days)
    number=df.index[i] #오류방지용 순서넣기

    if not makejungbok(jungbokcheck, df.loc[df.index[i],'고객명']): #중복이 아니면실행
        if df.loc[df.index[i],'몇주째']== gijun:
            pass
        else:
            gijun = df.loc[df.index[i], '몇주째'] #기준 업
            print() #\n누르기


        for j in range(len(dff)): #dff고객정보 의미
            if dff.loc[dff.index[j],'고객명'] == df.loc[df.index[i],'고객명']: #찾는것을 찾으면 정보 붙히기
                number = dff.loc[dff.index[j],'휴대폰']
                remaining = dff.loc[dff.index[j],'체류']

                for l in range(len(df2)): #df2 배달리스트에서 한 번 확인 (배달여부 체크)
                    if (df.loc[df.index[i],'고객명'] == df2.loc[df2.index[l],'고객명'])& (df2.loc[df2.index[l],'수거/배달'] =='배달') : #찾는게 있다면
                        CC='배달리스트 존재'

                if dff.loc[dff.index[j],'전화여부'] ==True: # 전화해야하는지 정보 확인
                    BB='전화'


            else:
                pass
        #number 값 획득

        print(df.loc[df.index[i], '고객명'], df.loc[df.index[i], '날짜차이'].days, number,'개수:',remaining ,BB,CC)



        numberlist.append((number,remaining))
        if df.loc[df.index[i],'고객명'] == '107-1304':
            print('평일 늦은 저녁에나 가능')
        jungbokcheck.append(df.loc[df.index[i],'고객명'])
        number= 'end' #number 초기화
        remaining = 0
        CC=""
        BB=''
    else:
        pass


print()
print()


jungbokcheck=[]

B = input('전화 번호 리스트 출력이면 0,1,2 or 전부')
if B=='0':
    pass


elif B=='1':
    for i in range(len(numberlist)):
        if numberlist[i][1]==1 and not makejungbok(jungbokcheck,numberlist[i][0]):
            print(numberlist[i][0])
            print()

elif B=='2':
    for i in range(len(numberlist)):
        if numberlist[i][1]>=2 and not makejungbok(jungbokcheck,numberlist[i][0]):
            print(numberlist[i][0])
            print()

else:
    for i in range(len(numberlist)):
        if not makejungbok(jungbokcheck,numberlist[i][0]):
            print(numberlist[i][0])
            print()




# print('기존전산기록확인')
# print('문자기록')
# print('배달리스트 체크')
# print('물건 메모 확인')

# (코트)오래된거 확인 주의 0번칸 외에 있는지보기
# (앱)배달예정확인
# (전산)배달리스트 돌려보면서 조회,물건개수 확인
# 실제 물건보기 있는지 여부와 메모확인
# 예약잡힌건 색깔바꾸기

