import pandas as pd
import datetime
import re

def contains_korean(text):
    #한글자라도 한글이 있는가?
    return re.search("[가-힣]+",text) #맞으면 값이 있고 없으면 NONE

def checkingtime():
    time= datetime.datetime.now()

    hour = time.hour
    weekday = time.weekday()
    if weekday == 0: # 월요일
        if hour <12:

            X='충전하기?'

        else:
            X='없음'


    elif weekday == 2: # 수요일
        if hour <12:
            X='비입주 문자돌리기, 물건 주문하기, 충전하기?'

        else:
            X='없음'


    elif weekday== 3: #목요일
        if hour <12:
            X='오래된거 확인하기 그리고 날씨 보고 오토바이 충전 생각'
        else:
            X= '비입주 전화돌리기'

    elif weekday == 4: #금요일
        if hour <12:
            X='오래된거 문자 보내기 그리고 오토바이 충전'
        else:
            X= '내일꺼 준비하기'

    elif weekday == 5: #토요일
        X='가게 주차시 직진해서 주차'


    else:
        X='없음'

    return X


def findingpassword(path, dict):
    # path = 'data.txt'

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split()  # 공백을기준으로 분리해 기억

            name, text= fields

            dict[name] = text


def printtingf(df, get_index, i, k):
    a = (df.loc[df.index[i], '수거/배달'], df.loc[df.index[i], '고객명'], df.loc[df.index[i], '요청일자'])
    get_index.append(df.index[i])
    globals()['get' + str(k)].append([a, df.loc[df.index[i], '동호수']])


df= pd.read_excel(r'C:\Users\user\Desktop\수거배달.xls')

noon=['09','10']
noon1=['11','12']
afternoon =['17','18','19','20']
early=['10']
sunsu=['115','114','113','112','111','110','109', '108', '107','106','105','104','103','102','101']

# sunsu= sunsu[::-1] #조절하는 기능


df = df[['수거/배달','고객명','요청일자']]
df['고객명'] = df['고객명'].apply(lambda x: x.split(' ')[-1])
df['요청일자'] = df['요청일자'].apply(lambda x: x.split('\n')[-1]).apply(lambda x: x[1:6])
df['동호수'] = df['고객명'].apply(lambda x: x.split('-')[0] if contains_korean(x) == None else x) #한글이 없으면 -앞에꺼, 있으면 그대로쓰기
df['시'] = df['요청일자'].apply(lambda x:x.split(':')[0])
df['분'] = df['요청일자'].apply(lambda x:x.split(':')[1])
df['문자이름'] = df['고객명'].apply(lambda x:False if contains_korean(x) == None else True ) #한글이 없으면 None이므로 False 있으면 True




plussunsu=[]
for o in range(len(df)): #문자이름 뽑아내기
    if df.loc[df.index[o],'문자이름'] == True:
        plussunsu.append(df.loc[df.index[o],'고객명'])

sunsu = plussunsu + sunsu #기존 순서문자열 앞에 추가해주기( 보통 가게라서 먼저가기 때문)
# print(sunsu)
# df= df[['순번', '등록일자', '요청일자', '수거/배달', '등록위치', '전화번호', '고객명', '주소', '상태', '수정']]


get_index=[]


get0=[]
get1=[]
get2=[]
get3=[]
get4=[]
get5=[]
get6=[]
get7=[]
get8=[]
get9=[]
get10=[]
get11=[]
get12=[]
get13=[]


k=0


for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] == '09': # 9시만
        if df.index[i] not in get_index :
            printtingf(df,get_index,i,k)


k= k+1


for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] == '10': # 10시만
        if df.index[i] not in get_index :
            #오전 걸러내기

            printtingf(df, get_index, i, k)



k= k+1

for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] == '11' and df.loc[df.index[i],'분']!='30' : #11시
        if df.index[i] not in get_index :
            #오전 걸러내기

            printtingf(df, get_index, i, k)


k= k+1

for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] == '11' and df.loc[df.index[i],'분']=='30'  : #11시 30분
        if df.index[i] not in get_index :
            #오전 걸러내기

            printtingf(df, get_index, i, k)



k= k+1

for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] == '12': #12시
        if df.index[i] not in get_index :
            #오전 걸러내기

            printtingf(df, get_index, i, k)



k= k+1


##오후

for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] in afternoon:



        if df.loc[df.index[i],'시']=='17'  and df.index[i] not in get_index :
            #오직 5시인경우

            printtingf(df, get_index, i, k)


k= k+1


for i in range(len(df)):
    if df.loc[df.index[i], '요청일자'][0:2] in afternoon:
        if df.loc[df.index[i],'시']=='18' and df.index[i] not in get_index : #6시 30분도 시간은 표시하되 저녁타임으로 생각

            printtingf(df, get_index, i, k)



k= k+1

for i in range(len(df)):
    if df.loc[df.index[i], '요청일자'][0:2] in afternoon:
        if df.loc[df.index[i],'시']=='18' and df.loc[df.index[i],'분']=='50' and df.index[i] not in get_index :
            # 6시 50분 즉 7시전까지 가야할것들

            printtingf(df, get_index, i, k)


k = k+1

for i in range(len(df)):
    if df.loc[df.index[i], '요청일자'][0:2] in afternoon:
        if df.loc[df.index[i],'시']=='19' and df.loc[df.index[i],'분']!='30' and df.index[i] not in get_index:
            printtingf(df, get_index, i, k)


k = k+1

for i in range(len(df)):
    if df.loc[df.index[i], '요청일자'][0:2] in afternoon:
        if df.loc[df.index[i],'시']=='19' and df.loc[df.index[i],'분']=='30'  and df.index[i] not in get_index:
            printtingf(df, get_index, i, k)


k = k+1

for i in range(len(df)):
    if df.loc[df.index[i], '요청일자'][0:2] in afternoon:
        if df.loc[df.index[i],'시']=='20' and df.loc[df.index[i],'분']=='00'  and df.index[i] not in get_index:
            printtingf(df, get_index, i, k)



k = k+1


for i in range(len(df)): #남은게 있다면 출력 (잘못된 시간대일경우 대비)
    if  df.index[i] not in get_index:
        printtingf(df, get_index, i, k)
        # print('???')
        # print(k)



c=[]


# print()
# print()
# print(df)




countingnumber=0
dict={} # password 담는용
text={} # 체크 포인트 담는용
findingpassword('data.txt',dict)
findingpassword('checkpoint.txt',text)
BB=''
AA=''

print(checkingtime())
for l in range(k+1): #모든 리스트 돌리기
    # print(globals()['get'+str(l)],l)
    for j in range(len(sunsu)):
        for i in range(len(globals()['get'+str(l)])):

            if globals()['get'+str(l)][i][1] == sunsu[j]: #동호수를꺼내서 15동부터 해당되는거 꺼내기


                if (globals()['get'+str(l)][i][0][2][-2:])=='10': # 무슨k, 튜플중 첫번째 정보, 그안에 있는 시간관련정보 중 miniute정보 가져오기
                    tem=(globals()['get'+str(l)][i][0][1])#동호수 입력
                    # print(tem)
                    BB = (dict.get(tem,'문앞'))

                # print(globals()['get'+str(l)][i][0][1]) # 정확한 이름임
                # print(text.get(globals()['get'+str(l)][i][0][1],'a'))

                if text.get(globals()['get'+str(l)][i][0][1],'a')!='a' : #주어진 동호수를 꺼냈는데 체크포인트에 내용이 있다면
                    AA=text.get(globals()['get'+str(l)][i][0][1],'')


                print(globals()['get'+str(l)][i][0] ,BB,AA)
                countingnumber= countingnumber + 1
                BB=''


                if (globals()['get'+str(l)][i][0][1]=='110-1504'):
                    print('호출금지')

                if globals()['get' + str(l)][i][0][1] in c: #중복1개당 1발언
                    print('중복존재')
                c.append(globals()['get' + str(l)][i][0][1])




                # print(l)
    print()

print(countingnumber,len(df.index))

