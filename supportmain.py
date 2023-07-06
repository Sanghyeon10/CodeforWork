import pandas as pd
import re
import copy
import datetime


def contains_korean(text):
    #한글자라도 한글이 있는가?
    return re.search("[가-힣]+",text) #맞으면 값이 있고 없으면 NONE


def checkingtime(df2,pricesum):
    time= datetime.datetime.now()

    hour = time.hour
    weekday = time.weekday()


    df2 = df2[df2['옷장번호'] == 0]
    df2 = df2[df2['비입주'] != '입주민']
    df2= df2[['고객명','날짜차이']]
    # df2= df2[df2['날짜차이']>datetime.timedelta(days=7)]
    df2['날짜차이']= df2['날짜차이'].apply(lambda x : str(x)).apply(lambda x : x.split(' ',1)[0])
    # df2['접수금액'] = df2['접수금액']
    for l in range(len(df2)): #칼럼추가해주기
        df2.loc[df2.index[l],'접수금액']= str(pricesum[df2.loc[df2.index[l],'고객명']])
    #
    # print(df2)
    # print(df2.values.flatten().tolist())
    df2 = df2.drop_duplicates(subset='고객명')
    Y= ', '.join(df2.values.flatten().tolist()) #리스트로 만든후에 문자열화
    # Y=df2.values.flatten().tolist()

    if weekday == 0: # 월요일
        if hour <12:

            X='충전하기'

        else:
            X='없음'


    elif weekday == 2: # 수요일
        if hour <12:
            X='1. 물건 주문하기 2. 충전하기'

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
        X='가게 주차시 직진해서 주차, 트렁크 비우기'


    else:
        X='없음'

    return X+':비입주는'+Y


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
    a = (df.loc[df.index[i], '수거/배달'], df.loc[df.index[i], '고객명'], df.loc[df.index[i], '요청일자'],df.loc[df.index[i], '동호수'] )
    get_index.append(df.index[i])
    globals()['get' + str(k)].append(a)

def mergeforget(list):
    newlist=copy.deepcopy(list)
    # print(list)
    # print(newlist)
    for j in range(len(list)):
        A = list[j][1]  # 기준이 될 고객명 j번째
        B = list[j][0]  # 배달수거 문자열 저장된것
        for i in range(len(list)): #전체를 검사한다 그리고 그것을 전체 반복할것
            if A == list[i][1] and B!= list[i][0]: #이름은 같되 배달 수거가 다른것이 있다면 새로운것으로 재탄생
                temp = ('수거배달', list[i][1],list[i][2],list[i][3] ) #개수 4개로 맞춰주기
                if temp not in newlist: #고객명이 안들어있으면
                    newlist.append(temp)
                    newlist.remove(list[j])
                    newlist.remove(list[i])


    return newlist



def getdf1():
    df = pd.read_excel(r'C:\Users\user\Desktop\수거배달.xls')

    df = df[['수거/배달', '고객명', '요청일자','등록일자']]
    df['고객명'] = df['고객명'].apply(lambda x: x.split(' ')[-1])
    df['요청일자'] = df['요청일자'].apply(lambda x: x.split('\n')[-1]).apply(lambda x: x[1:6])
    df['등록일자'] = pd.to_datetime( df['등록일자'].apply(lambda x: "20"+x.split('\n')[0] +" " + x.split('\n')[-1][1:6] )) #datetime형태로 시간저장

    df['동호수'] = df['고객명'].apply(lambda x: x.split('-')[0] if contains_korean(x) == None else x)  # 한글이 없으면 -앞에꺼, 있으면 그대로쓰기
    df['시'] = df['요청일자'].apply(lambda x: x.split(':')[0])
    df['분'] = df['요청일자'].apply(lambda x: x.split(':')[1])
    df['문자이름'] = df['고객명'].apply(lambda x: False if contains_korean(x) == None else True)  # 한글이 없으면 None이므로 False 있으면 True

    # print(df)
    return df

def getdf2():
    df2 = pd.read_excel(r'C:\Users\user\Desktop\옷장조회.xls')
    df2 = df2[['접수일자', '완성일자', '고객명', '옷장번호', '택번호', '상품명']]
    # df2 = df2.dropna()
    df2= df2.fillna(method='ffill')
    df2 = df2.drop_duplicates(subset='택번호')
    df2['고객명'] = df2['고객명'].apply(lambda x: x.split('\n')[0])
    df2['비입주'] = df2['고객명'].apply(lambda x: x.split('-')[0] if contains_korean(x) != None else '입주민')

    df2['접수일자'] = df2['접수일자'].apply(lambda x: x.split('\n')[0]).apply(lambda x: '20' + x)
    df2['완성일자'] = df2['완성일자'].apply(lambda x: x.split('\n')[0]).apply(lambda x: '20' + x)
    df2['접수일자'] = df2['접수일자'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    df2['완성일자'] = df2['완성일자'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    df2['날짜차이'] = datetime.datetime.now() - df2['완성일자']
    df2['동호수'] = df2['고객명'].apply(lambda x: x.split('-')[0] if contains_korean(x) == None else x)
    df2['택숫자'] = df2['택번호'].apply(lambda x: int(x.replace("-","")) if "-" in x else None ) #-있으면 숫자화 아니면 '사용안함'이므로 None처리
    # print(df2)
    return df2

def getpastSat(df1,df2):
    ## 지난주 토요일날까지 완성된것 리스트 중 오늘 배달갈곳의 동수가 일치되는지 구하는 것.
    now = datetime.datetime.now()
    week = now.weekday() + 2
    pastSat = now - datetime.timedelta(days=(week))
    pastpastSat = now - datetime.timedelta(days=(week) + 7)
    # print(pastSat)
    lastSatdf = df2[df2['완성일자'] <= pastSat]
    lastSatdf = lastSatdf[lastSatdf['옷장번호'] == 0]
    lastSatdf = lastSatdf[lastSatdf['비입주'] == '입주민']
    lastSatdf = lastSatdf[['고객명', '동호수']]

    lastSatdf = (lastSatdf[lastSatdf['동호수'].isin(df1['동호수'])])

    lastSatdf = lastSatdf[['고객명']]
    # print( lastSatdf.values.flatten().tolist() )

    lastlastSatdf = df2[df2['완성일자'] <= pastpastSat]
    lastlastSatdf = lastlastSatdf[lastlastSatdf['옷장번호'] == 0]
    lastlastSatdf = lastlastSatdf[lastlastSatdf['비입주'] == '입주민']
    lastlastSatdf = lastlastSatdf[['고객명', '동호수']]

    lastlastSatdf = (lastlastSatdf[lastlastSatdf['동호수'].isin(df1['동호수'])])
    lastlastSatdf = lastlastSatdf[['고객명']]
    # print(lastlastSatdf)

    return lastSatdf, lastlastSatdf


def getdf4():
    df4 = pd.read_excel(r'C:\Users\user\Desktop\옷장조회.xls')
    df4 = df4.fillna(method='ffill')
    df4['고객명'] = df4['고객명'].apply(lambda x: x.split('\n')[0])

    df4 = df4[['고객명', '상품명', '접수금액','택번호']]


    df4['접수금액'] = df4['접수금액'].apply(lambda x: int(x.replace(",", "")))
    price_sum = df4.groupby('고객명')['접수금액'].sum() / 1000

    df4 = df4.drop_duplicates(subset='택번호')

    df4['택숫자'] = df4['택번호'].apply(lambda x: int(x.replace("-", "")) if "-" in x else None)
    df4['숫자차이'] = df4['택숫자'].diff().fillna(1)
    item_count = df4.groupby('고객명')['상품명'].count()
    diffnumber= df4.groupby('고객명')['숫자차이'].apply(lambda x : x.iloc[1:].sum()) #첫행은 관련이 없으므로 제외.

    tempdf= df4['상품명'].copy()

    df4['상품명'] = tempdf.str.contains("운동화|골프화|신발|아동화|등산화|가방|구두|부츠|에코백|이불|커버|담요|시트|인형|매트").apply(
        lambda x: x if x == True else None)
    gita_count= df4.groupby('고객명')['상품명'].count()

    df4['상품명'] =  tempdf.str.contains("운동화|골프화|신발|아동화|등산화|가방|구두|부츠|에코백").apply(
        lambda x: x if x == True else None)
    shoe_count = df4.groupby('고객명')['상품명'].count()

    df4['상품명'] =  tempdf.str.contains("이불|커버|담요|시트|인형|매트").apply(
        lambda x: x if x == True else None)
    bedding_count= df4.groupby('고객명')['상품명'].count()


    return item_count,gita_count, shoe_count , bedding_count,diffnumber ,   price_sum


def getdf3():

    df3 = pd.read_excel(r'C:\Users\user\Desktop\고객정보.xls')
    df3= df3[['고객명','휴대폰','체류','주소','특이사항',"총미수금"]]
    df3.fillna('',inplace=True)
    # df3= df3.dropna(axis=0)
    df3['고객명'] = df3['고객명'].apply(lambda x: x.split('\n')[0])
    df3['전화여부'] = df3[['주소','특이사항']].apply(lambda x:'전화' in ''.join(x),axis=1)

    return df3

if __name__ =="__main__":
    #주소 특이사항에 전화있는 사람 목록 뽑는 코드
    df =getdf3()
    df[df['전화여부']==True]['고객명'].to_csv('juso.txt',index=False)
    # print(df)