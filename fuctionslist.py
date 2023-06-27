import pandas as pd
import re
import copy
import datetime



def contains_korean(text):
    #한글자라도 한글이 있는가?
    return re.search("[가-힣]+",text) #맞으면 값이 있고 없으면 NONE

def checkingtime():
    time= datetime.datetime.now()

    hour = time.hour
    weekday = time.weekday()
    if weekday == 0: # 월요일
        if hour <12:

            X='충전하기'

        else:
            X='없음'


    elif weekday == 2: # 수요일
        if hour <12:
            X='1.비입주 문자돌리기 2. 물건 주문하기 3. 충전하기?'

        else:
            X='없음'


    elif weekday== 3: #목요일
        if hour <12:
            X='1.오래된거 확인하기,2. 오토바이 충전 생각'
        else:
            X= '비입주 전화돌리기'

    elif weekday == 4: #금요일
        if hour <12:
            X='1.오래된거 문자 보내기 2. 오토바이 충전'
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

            name= line.split(" ",1)[0]

            text = line.split(" ",1)[1]
            text = text.rstrip('\n')
            # fields = line.strip().split()  # 공백을기준으로 분리해 기억

            # name, text= fields

            dict[name] = text


def printtingf(df, get_index, i, k):
    a = (df.loc[df.index[i], '수거/배달'], df.loc[df.index[i], '고객명'], df.loc[df.index[i], '요청일자'])
    get_index.append(df.index[i])
    globals()['get' + str(k)].append([a, df.loc[df.index[i], '동호수']])

def mergeforget(list):
    newlist=copy.deepcopy(list)
    for j in range(len(list)):
        A = list[j][0][1]  # 기준이 될 고객명 j번째
        B = list[j][0][0]  # 배달수거 문자열 저장된것
        for i in range(len(list)): #전체를 검사한다 그리고 그것을 전체 반복할것
            if A == list[i][0][1] and B!= list[i][0][0]: #이름은 같되 배달 수거가 다른것이 있다면 새로운것으로 재탄생
                temp = ('수거배달', list[i][0][1],list[i][0][2])
                if [temp,list[i][1]] not in newlist: #안들어있으면
                    newlist.append([temp,list[i][1]])
                    newlist.remove(list[j])
                    newlist.remove(list[i])

    return newlist

def makejungbok(listt,X):
    if X in listt: #값이 있다.
        return True#중복임

    else:
        listt.append(X)
        return False #값이 없으니까 중복아님

def makedf1():

    df1= pd.read_excel(r'C:\Users\user\Desktop\수거배달.xls')
    df1 = df1[['수거/배달','고객명','요청일자']]
    df1['고객명'] = df1['고객명'].apply(lambda x: x.split(' ')[-1])
    df1['날짜'] = df1['요청일자'].apply(lambda x: x.split('\n')[0])
    df1['날짜'] = df1['날짜'].apply(lambda x: datetime.datetime.strptime(x, '%y-%m-%d'))
    df1['요청일자'] = df1['요청일자'].apply(lambda x: x.split('\n')[-1]).apply(lambda x: x[1:6])
    df1['시'] = df1['요청일자'].apply(lambda x:x.split(':')[0])
    df1['분'] = df1['요청일자'].apply(lambda x:x.split(':')[1])
    df1['동호수'] = df1['고객명'].apply(lambda x: x.split('-')[0] if contains_korean(x) == None else x) #한글이 없으면 -앞에꺼, 있으면 그대로쓰기
    df1['문자이름'] = df1['고객명'].apply(lambda x:False if contains_korean(x) == None else True ) #한글이 없으면 None이므로 False 있으면 True

    return df1

def makedf2():
    df2 = pd.read_excel(r'C:\Users\user\Desktop\옷장조회.xls')
    df2= df2[['접수일자','완성일자', '고객명','옷장번호','택번호','상품명']]
    df2 = df2.fillna(method='ffill')
    df2['고객명'] = df2['고객명'].apply(lambda x: x.split('\n')[0])

    df2['접수일자']= df2['접수일자'].apply(lambda x: x.split('\n')[0]).apply(lambda x: '20'+x)
    df2['완성일자']= df2['완성일자'].apply(lambda x: x.split('\n')[0]).apply(lambda x: '20'+x)
    df2['비입주']=df2['고객명'].apply(lambda x: x.split('-')[0] if contains_korean(x) != None else '입주민')

    df2=df2[df2['옷장번호']==0]


    df2['접수일자'] = df2['접수일자'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    df2['완성일자'] = df2['완성일자'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    df2['몇주째'] = df2['완성일자'].apply(lambda x: x.strftime("%U"))

    df2['날짜차이'] = df2['완성일자'] - df2['접수일자']

    #비입주 조절용
    # df2=df2[df2['비입주']==A]

    # now = datetime.datetime.now()  # + datetime.timedelta(days=3)
    # week = now.weekday() + day
    # pastSat = now - datetime.timedelta(days=(week))
    #
    # df2 = df2[df2['완성일자'] <= pastSat]

    return df2


def makedf3():

    df3 = pd.read_excel(r'C:\Users\user\Desktop\고객정보.xls')
    df3= df3[['고객명','휴대폰','체류','주소','특이사항']]
    df3.fillna('',inplace=True)
    # df3= df3.dropna(axis=0)
    df3['고객명'] = df3['고객명'].apply(lambda x: x.split('\n')[0])
    df3['전화여부'] = df3[['주소','특이사항']].apply(lambda x:'전화' in ''.join(x),axis=1)

    return df3


#주소 특이사항에 전화있는 사람 목록 뽑는 코드
df =makedf3()
df[df['전화여부']==True]['고객명'].to_csv('juso.txt',index=False)
