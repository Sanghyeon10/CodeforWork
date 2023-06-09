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

def findingpassword(path, dict):
    # path = 'data.txt'

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:

            name= line.split(" ",1)[0]

            text = line.split(" ",1)[1]
            text = text.rstrip('\n')
            # fields = line.strip().split()  # 공백을기준으로 분리해 기억

            # name, text= fields

            dict[name] = text



now = datetime.datetime.now() #+ datetime.timedelta(days=3)
print('오늘날짜',now)

inputt='b' # input('비입주이면 a입력, 배달리스트 토요일까지 껄로 했나?')
print('배달리스트 토요일까지 껄로 했나?')
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


#운동화개수, 그냥개수 구하기
df4 = pd.read_excel(r'C:\Users\user\Desktop\옷장조회.xls')
df4=df4.fillna(method='ffill')

df4= df4.drop_duplicates(subset='택번호')
df4['고객명'] = df4['고객명'].apply(lambda x: x.split('\n')[0])
df4= df4[['고객명','상품명']]
item_count= df4.groupby('고객명')['상품명'].count()

# print( df4['상품명'].str.contains("운동화|골프화|신발|아동화|등산화|가방|구두|부츠|에코백") )
df4['상품명'] = df4['상품명'].str.contains("운동화|골프화|신발|아동화|등산화|가방|구두|부츠|에코백|이불|커버|담요|시트|인형|매트").apply(lambda x : x if x == True else None)
shoe_count= df4.groupby('고객명')['상품명'].count()


#기타사항 가져오기
dictt={}
gita= findingpassword('gita.txt',dictt)


numberlist=[]
remaining=0 #남아있는거 세는 변수
jungbokcheck=[]
BB=''
CC=''
gijun=df.loc[df.index[0],'몇주째']
tempremaining=""

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
                if dff.loc[dff.index[j],'체류']!=item_count[dff.loc[dff.index[j],'고객명']]:
                    tempremaining='XXX'
                else:
                    tempremaining=""

                remainings = str(dff.loc[dff.index[j],'체류'])+','+str(item_count[dff.loc[dff.index[j],'고객명']])+'('+str(shoe_count[dff.loc[dff.index[j],'고객명']]) + ')'+tempremaining
                totalremaining = int(dff.loc[dff.index[j],'체류'])
                inventories= int(item_count[dff.loc[dff.index[j],'고객명']])
                # print(dff.loc[dff.index[j],'체류']==item_count[dff.loc[dff.index[j],'고객명']])

                for l in range(len(df2)): #df2 배달리스트에서 한 번 확인 (배달여부 체크)
                    if (df.loc[df.index[i],'고객명'] == df2.loc[df2.index[l],'고객명'])& (df2.loc[df2.index[l],'수거/배달'] =='배달') : #찾는게 있다면
                        CC='배달리스트 존재'

                if dff.loc[dff.index[j],'전화여부'] ==True: # 전화해야하는지 정보 확인
                    BB='전화'

                if dictt.get(dff.loc[dff.index[j],'고객명'],'a')!='a' : #주어진 고객명을 검색했는데 기타텍본에 내용이 있다면
                    BB= BB + dictt.get(dff.loc[dff.index[j],'고객명'],'a')

            else:
                pass
        #number 값 획득

        print(df.loc[df.index[i], '고객명'], df.loc[df.index[i], '날짜차이'].days, number,'개수:',remainings ,BB,CC)



        numberlist.append((number,totalremaining,inventories,df.loc[df.index[i], '고객명']))
        # if df.loc[df.index[i],'고객명'] == '107-1304':
        #     print('평일 늦은 저녁에나 가능')

        jungbokcheck.append(df.loc[df.index[i],'고객명'])
        number= 'end' #number 초기화
        remaining = 0
        totalremainings = ''
        inventories=""
        CC=""
        BB=''
    else:
        pass


print()
print()


jungbokcheck=[]
forprintdf=pd.Series(dtype='object')
notpirnt=["110-2202"] #출력하지 않을 동호수

B = input('전화 번호 리스트 출력이면 0,1,2 or 전부')
if B=='0':
    pass


elif B=='1':
    for i in range(len(numberlist)):
        if numberlist[i][1]==1 and not makejungbok(jungbokcheck,numberlist[i][0]):
            print(numberlist[i][0])
            print()
            if numberlist[i][1] == numberlist[i][2] and numberlist[i][3] not in notpirnt : #재고개수와 완성개수가 같다면 프린트목록에 해당.
                pass
                # forprintdf.append(numberlist[i][0])

elif B=='2':
    for i in range(len(numberlist)):
        if numberlist[i][1]>=2 and not makejungbok(jungbokcheck,numberlist[i][0]):
            print(numberlist[i][0])
            print()
            if numberlist[i][1] == numberlist[i][2] and numberlist[i][3] not in notpirnt : #재고개수와 완성개수가 같다면 프린트목록에 해당.
                pass
                # forprintdf.append(numberlist[i][0])

else:
    for i in range(len(numberlist)):
        if not makejungbok(jungbokcheck,numberlist[i][0]):
            print(numberlist[i][0])
            print()
            if numberlist[i][1] == numberlist[i][2] and numberlist[i][3] not in notpirnt: #재고개수와 완성개수가 같다면 프린트목록에 해당.
                pass
                # forprintdf.append(numberlist[i][0])


with open('checkpoint.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if "010" in line:
            forprintdf= pd.concat([forprintdf, pd.Series(line.rstrip("\n"))])



# forprintdf =pd.DataFrame(forprintdf,columns=['전화번호'])
forprintdf.name='전화번호'
print(forprintdf)
forprintdf.to_csv('전화번호리스트.csv',index=False)






# print('기존전산기록확인')
# print('문자기록')
# print('배달리스트 체크')
# print('물건 메모 확인')

# (코트)오래된거 확인 주의 0번칸 외에 있는지보기
# (앱)배달예정확인
# (전산)배달리스트 돌려보면서 조회,물건개수 확인
# 실제 물건보기 있는지 여부와 메모확인
# 예약잡힌건 색깔바꾸기

