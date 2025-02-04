import pandas as pd
import re
import copy
import datetime
import afternoontime
import numpy as np
pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.expand_frame_repr', False)  # 가로로 스크롤 없이 출력

def contains_korean(text):
    #한글자라도 한글이 있는가?
    return re.search("[가-힣]+",text) #맞으면 값이 있고 없으면 NONE

def check_words_in_string(word_list, input_string):
    #실제가 아닌것들0
    # print(any(word in input_string for word in word_list) )
    # print(input_string)
    return any(word in input_string for word in word_list) #맞으면 Ture 아니면 False



def checkingtime(df2,price_sum,df3,item_count):
    time= datetime.datetime.now()

    hour = time.hour
    weekday = time.weekday()

    # print(item_count.keys())

    df2 = df2[df2['옷장번호'] == 0]
    df2 = df2[df2['비입주'] != '입주민']
    df2= df2[['고객명','날짜차이',"완성일자"]]
    # df2= df2[df2['날짜차이']>datetime.timedelta(days=7)]
    df2['날짜차이']= df2['날짜차이'].apply(lambda x : str(x)).apply(lambda x : x.split(' ',1)[0]).apply(lambda x : int(x))
    #정렬을 위해 정수화해주기
    # df2['접수금액'] = df2['접수금액']
    for l in range(len(df2)): #칼럼추가해주기
        if df3.loc[df2.loc[df2.index[l],'고객명'], '체류']== item_count[df2.loc[df2.index[l],'고객명']]:#개수 같으면 문자열로 숫자입력 부분완성은 -1
            df2.loc[df2.index[l],'접수금액']= str(price_sum[df2.loc[df2.index[l],'고객명']])
        else:
            df2.loc[df2.index[l], '접수금액'] = str(-1)
        # print(df2.loc[df2.index[l],'고객명'])

    # print(df2.values.flatten().tolist())
    df2 = df2.sort_values(by='완성일자', ascending=False).drop_duplicates(subset='고객명', keep='first') #가장 최신날짜만 남기기
    # df2 = df2.drop_duplicates(subset='고객명',keep='last')
    df2 = df2.sort_values(by="날짜차이",ascending=False) # 오래된거 기준으로 정렬해주기 그러면 가장 늦은 완성일기준으로 몇일 지난지 표시해주는것임.
    # print(len(df2))
    if len(df2)!=0: #남아있는 비입주 재고있을때에만
        # print(df2)
        df2 = df2[['고객명', '날짜차이','접수금액']]

        #정렬후에는 문자열 합치기를 위해서 다시 문자열화
        df2['날짜차이'] = df2['날짜차이'].apply(lambda x: str(x))
        df2=df2[df2['접수금액']!=str(-1)] #접수금액이 -1이면 일부 미완성이라 drop해서 날리기

        # print(df2)
        Y= ', '.join(df2.values.flatten().tolist()) #리스트로 만든후에 문자열화

        df2['접수금액'] = df2['접수금액'].apply(lambda x: float(x))
        df2 = df2[df2['접수금액']>=30]
        df2 =df2['고객명']
        # print(df2.values)
    else:
        df2=pd.DataFrame()
        Y=""

    if weekday == 0: # 월요일
        if hour <12:
            X='충전하기'

        else:
            X='없음'

    elif weekday == 1: # 화요일
        if hour <12:

            X='옷걸이 박스 개수 세기'

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

    return X +':비입주는 '+Y , df2.values #df2.value는 특정 금액대 이상의 비입주



def findingpassword(path, dict):
    # path = 'data.txt'

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:

            name= line.split(" ",1)[0]

            text = line.split(" ",1)[1]
            text = text.rstrip('\n')
            # fields = line.strip().split()  # 공백을기준으로 분리해 기억

            # name, text= fields
            if name not in dict.keys(): #혹시 2개의 키가 중복될때 쓰이는 부분
                dict[name] = text
            else:
                dict[name] = dict[name] +"," + text


def printtingf(df, get_index, i, k):
    a = (df.loc[df.index[i], '수거/배달'], df.loc[df.index[i], '고객명'], df.loc[df.index[i], '요청일자'],df.loc[df.index[i], '동호수'] )
    get_index.append(df.index[i])
    globals()['get' + str(k)].append(a)

def lastpiece(X):
    a=X[-1:] #마지막 글자만 슬라이싱
    if a.isdigit() :#문자열로된 숫자라면
        a= int(a)
    else:
        a=0

    return a


def mergeforget(list):
    newlist=copy.deepcopy(list)
    # print(list)
    # print(newlist)
    for j in range(len(list)):
        try:
            A = list[j][1]  # 기준이 될 고객명 j번째
            B = list[j][0]  # 배달수거 문자열 저장된것
            for i in range(len(list)): #전체를 검사한다 그리고 그것을 전체 반복할것
                if A == list[i][1] and B!= list[i][0]: #이름은 같되 배달 수거가 다른것이 있다면 새로운것으로 재탄생
                    temp = ('수거배달', list[i][1],list[i][2],list[i][3], list[i][4] ) #개수 5개로 맞춰주기
                    if temp not in newlist: #고객명이 안들어있으면
                        newlist.append(temp)
                        newlist.remove(list[j])
                        newlist.remove(list[i])
                        #만약 10분 부분이 불일치하면, 그 동호수 수거배달이 2개가 됨.
        except Exception as e:
            print("An error occurred:", e, list[j])
    # print(newlist)
    return newlist

def getorderwithprice( price_sum,set, df3,item_count):
    # 미수금을 기준으로 내림차순으로 정렬된 리스트 생성
    price_sum = sorted(price_sum.items(), key=lambda x: x[1], reverse=True)

    # 결과를 저장할 리스트 초기화
    result_list = []

    # 결과 리스트에 이름과 미수금 정보 추가
    for name, debt in price_sum:
        if name in set and debt > 0.0:
            if (df3.loc[name,'체류'])!= item_count[name]:# 불일치 하면 +표시
                result_list.append(f'{name}({debt})+')
            else:
                result_list.append(f'{name}({debt})')
    return  result_list

def getPotentialBaedalList( df2,set ):
    # 결과를 저장할 리스트 초기화
    result_list = []

    for name in set: #각이름에 대하여 택숫자 가져오기
        for i in range(len(df2)):
            if df2.loc[df2.index[i],'고객명']== name:
                result_list.append(df2.loc[df2.index[i],'택번호'])
                break


    return  result_list


def getdf1():
    df = pd.read_excel(r'C:\Users\user\Desktop\수거배달.xls')

    df = df[['수거/배달', '고객명', '요청일자','등록일자']]
    df['고객명'] = df['고객명'].apply(lambda x: x.split(' ')[-1])

    df['요청일자일자'] = pd.to_datetime( df['요청일자'].apply(lambda x: "20"+x.split('\n')[0] +" " + x.split('\n')[-1][1:6] ))
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

    df2 = df2[df2['옷장번호'] == 0] #옷장번호 0번 외에것은 무시하기
    # df2 = df2.dropna()
    df2= df2.fillna(method='ffill')
    df2['택번호'] = df2['택번호'].where(df2['택번호'] != '사용안함', df2.groupby('택번호').cumcount().add(1).map(lambda x: f"사용안함{x}"))

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
    # 후예약은 대쉬보드에서 집합으로 제외해줌. 여기서는 오늘치껏만 계산.
    now = datetime.datetime.now()
    week = now.weekday() + 2
    pastSat = now - datetime.timedelta(days=(week))
    pastpastSat = now - datetime.timedelta(days=(week) + 7)
    # print(pastSat)
    lastSatdf = df2[df2['완성일자'] <= pastSat]
    lastSatdf = lastSatdf[lastSatdf['옷장번호'] == 0]
    lastSatdf = lastSatdf[lastSatdf['비입주'] == '입주민']
    lastSatdf = lastSatdf[['고객명', '동호수']]

    fulllist= lastSatdf[['고객명']]

    lastSatdf = (lastSatdf[lastSatdf['동호수'].isin(df1['동호수'])]) #동수가 같은것 골라내는 것

    lastSatdf = lastSatdf[['고객명']]
    # print( lastSatdf.values.flatten().tolist() )

    lastlastSatdf = df2[df2['완성일자'] <= pastpastSat]
    lastlastSatdf = lastlastSatdf[lastlastSatdf['옷장번호'] == 0]
    lastlastSatdf = lastlastSatdf[lastlastSatdf['비입주'] == '입주민']
    lastlastSatdf = lastlastSatdf[['고객명', '동호수']]

    calllist = lastlastSatdf[['고객명']]
    lastlastSatdf = (lastlastSatdf[lastlastSatdf['동호수'].isin(df1['동호수'])])
    lastlastSatdf = lastlastSatdf[['고객명']]
    # print(lastlastSatdf)

    allofalllist=df2[df2['옷장번호'] == 0]
    allofalllist = allofalllist[allofalllist['비입주'] == '입주민']
    allofalllist= allofalllist[['고객명', '동호수']]
    # print('dff',df2)

    return lastSatdf, lastlastSatdf, calllist, fulllist ,allofalllist


def getdf4():
    df4 = pd.read_excel(r'C:\Users\user\Desktop\옷장조회.xls')
    df4 = df4.fillna(method='ffill')
    df4['택번호'] = df4['택번호'].where(df4['택번호'] != '사용안함', df4.groupby('택번호').cumcount().add(1).map(lambda x: f"사용안함{x}"))

    df4['고객명'] = df4['고객명'].apply(lambda x: x.split('\n')[0])

    df4 = df4[['고객명', '상품명', '접수금액','택번호']]
    # print(df4)

    df4['접수금액'] = df4['접수금액'].apply(lambda x: int(x.replace(",", "")))
    price_sum = df4.groupby('고객명')['접수금액'].sum() / 1000
    # print('price',price_sum)
    df4 = df4.drop_duplicates(subset='택번호') #가격을 다 더한후에 중복택을 날려야 개수와 가격 둘다 문제 없음


    df4['택숫자'] = df4['택번호'].apply(lambda x: int(x.replace("-", "")) if "-" in x else None)
    #-이 없으면 사용안함문자열이므로 None 결측치 처리하기
    df4['숫자차이'] = df4['택숫자'].diff().fillna(1)
    # df4.to_csv('testtest.csv')
    # print(df4)
    item_count = df4.groupby('고객명')['상품명'].count()

    

    # 'Name'을 기준으로 그룹화한 후, 'Number' 칼럼 값의 차이 구하기
    grouped_df = df4.groupby('고객명')['택숫자'].diff()
    # print(type(grouped_df))
    # 'Name'을 기준으로 그룹화한 후, 'Number' 칼럼 값의 차이의 누적합 구하기
    cumulative_sum = grouped_df.groupby(df4['고객명']).cumsum()
    # print(cumulative_sum)
    # 모든 사람의 마지막 값 출력
    diffnumber = cumulative_sum.groupby(df4['고객명']).last().fillna(0)

    # print(diffnumber)
    # grouped_df.to_csv('testtest.csv')




    tempdf= df4['상품명'].copy()

    df4['상품명'] = tempdf.str.contains("어그|운동화|골프화|신발|아동화|등산화|가방|구두|부츠|에코백|이불|커버|담요|시트|인형|매트|카페트|커텐|커튼|배게").apply(
        lambda x: x if x == True else None)
    gita_count= df4.groupby('고객명')['상품명'].count()

    df4['상품명'] =  tempdf.str.contains("어그|운동화|골프화|신발|아동화|등산화|가방|구두|부츠|에코백").apply(
        lambda x: x if x == True else None)
    shoe_count = df4.groupby('고객명')['상품명'].count()

    df4['상품명'] =  tempdf.str.contains("이불|커버|담요|시트|인형|매트|카페트|커텐|커튼|배게").apply(
        lambda x: x if x == True else None)
    bedding_count= df4.groupby('고객명')['상품명'].count()

    df4['상품명'] = tempdf.str.contains("기장|수선|누빔|단뜸|견본|지퍼").apply(
        lambda x: x if x == True else None)
    susun_count = df4.groupby('고객명')['상품명'].count()

    df4['상품명'] = tempdf.str.contains("원피스|코트|한복").apply(
        lambda x: x if x == True else None)
    long_count = df4.groupby('고객명')['상품명'].count()

    df4['상품명'] = tempdf.str.contains("보류|재작업|세탁불가").apply(
        lambda x: x if x == True else None)
    shoulcheck_count = df4.groupby('고객명')['상품명'].count()


    return item_count,gita_count, shoe_count , bedding_count,diffnumber , susun_count,long_count,  price_sum ,shoulcheck_count


def getdf3():

    df3 = pd.read_excel(r'C:\Users\user\Desktop\고객정보.xls')
    df3= df3[['고객명','휴대폰','체류','주소','특이사항',"총미수금"]]
    df3.fillna('',inplace=True)
    # df3= df3.dropna(axis=0)
    df3['총미수금'] = df3['총미수금'].apply(lambda x: int(x.replace(",", "")))
    df3['총미수금'] = df3['총미수금']/1000
    df3['체류'] = df3['체류'].apply(lambda x: int(x))
    df3['고객명'] = df3['고객명'].apply(lambda x: x.split('\n')[0])
    df3['전화여부'] = df3[['주소','특이사항']].apply(lambda x:'전화' in ''.join(x),axis=1)

    return df3


def getdf5(): # 미래에 예약된거 찾아보기
    df5= pd.read_excel(r'C:\Users\user\Desktop\후예약.xls')
    if '수거/배달' in df5.columns: #수거배달 미래치인 경우
        df5 = df5[['수거/배달', '고객명','요청일자']]
        df5['고객명'] = df5['고객명'].apply(lambda x: x.split(' ')[-1])
        df5['요청일자'] = pd.to_datetime( df5['요청일자'].apply(lambda x: "20"+x.split('\n')[0] +" " + x.split('\n')[-1][1:6] )) #datetime형태로 시간저장

        today = datetime.datetime.now()
        if df5.loc[df5.index[0],'요청일자'].date()== today.date() :# 첫번째 정보가 오늘날짜와 같다면 비업데이트는 아님.
            df5= df5[df5['수거/배달']=='배달'] #배달예약만 의미있음.
            df5= df5[['고객명']] #이것만 살리기
            df5= df5.values.flatten().tolist()


        else:

            df5=[] #업데이트 안된 파일이므로 쓸모없는 정보임.
            # print('됸')

        print('후예약')

    else:# 접수목록리스트인경우
        df5 = df5[['접수일자', '고객명',  '택번호', '상품명','진행']]

        # df5 = df5.dropna()
        df5 = df5.fillna(method='ffill')
        df5['택번호'] = df5['택번호'].where(df5['택번호'] != '사용안함', df5.groupby('택번호').cumcount().add(1).map(lambda x: f"사용안함{x}"))
        df5 = df5.drop_duplicates(subset='택번호')
        df5['진행'] = df5['진행'].apply(lambda x: int(x))
        df5 = df5[df5['진행']!=4] # 4출고 3 완성 0 접수

        conditions = [(df5['진행'] == 4),(df5['진행'] == 3),(df5['진행'] == 0)]
        choices = ['(출고)', '(완성)', '(접수)']


        df5['고객명'] = df5['고객명'].apply(lambda x: x.split('\n')[0])

        # df5['상품명'] = df5['상품명'].where(df5['진행'] != 3,  df5['상품명'] + '(완성)')
        df5['상품명'] =  df5['상품명'] + np.select(conditions, choices, default='')
        df5['접수일자'] = df5['접수일자'].apply(lambda x: x.split('\n')[0]).apply(lambda x: '20' + x)
        df5['접수일자'] = df5['접수일자'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

        # print(df5)
        # print(type(datetime.datetime.now().date()))
        today= datetime.datetime.now().date()
        df5['날짜차이'] = datetime.datetime.now() - df5['접수일자']

        if df5.empty:
            df5=pd.DataFrame()

        else:
            checkpoint = (df5.loc[df5.index[-1],'접수일자']).date()

            if (today-checkpoint).days !=0  : # 오늘 날짜 포함, 살릴지 여부 설정으로 판단
                if afternoontime.jubsulist == True:
                    pass
                else:
                    df5=pd.DataFrame()

        print('접수목록 리스트' ,len(df5))
        # print(df5)


    return df5


def remove_duplicates_preserve_order(input_list):
    output_list = []
    for item in input_list:
        if item not in output_list:
            output_list.append(item)
    return output_list



def getdiffrentwangsung(df,ID):
    # 고객별로 그룹화
    customer_grouped = df.groupby('고객명')


    # 각 고객별로 "접수일자"별로 다시 그룹화
    result = customer_grouped.apply(
        lambda group: group.groupby('접수일자').apply(lambda sub_group: sub_group['완성일자'].max() - sub_group['완성일자'].min()))

    if len(result) !=1: #고객 한명만 있으면 이유는 모르는데 에러남.

        # 시리즈에서 인덱스 추출(시리즈 안에 시리즈 있어서 2번 접근하는것임)
        index_values = result[ID].index
        # 첫 번째와 마지막 인덱스 선택
        first_index = index_values[0]
        last_index = index_values[-1]
        # # 결과 출력
        # print("첫 번째 인덱스:", first_index)
        # print("마지막 인덱스:", last_index)
        # 합까지 구하기 가능
        data = result[ID].loc[first_index:last_index].values
        total_days = data.astype('timedelta64[D]').sum().astype(int)

        return total_days

    else:
        return 0


def GetNonharingtonMemo(input_string):
    try:
        # 현재 날짜 가져오기
        current_date = datetime.datetime.now()

        # 문자열에서 8자리 연속된 숫자 추출
        date_strings = re.findall(r'\d{8}', input_string)

        for date_str in date_strings:
            try:
                # 8자리 숫자를 날짜로 변환
                date = datetime.datetime.strptime(date_str, '%Y%m%d')

                # 현재 날짜와의 차이 계산
                delta = current_date - date

                # 새로운 문자열로 8자리 숫자 대체
                input_string = input_string.replace(date_str, f'{delta.days} days')

            except ValueError:
                # 날짜 형식이 잘못된 경우 무시
                pass

    except Exception as e:
        # 예외 처리 (원하는 방식으로 처리)
        print(f"에러 발생: {str(e)}")

    return input_string


def BeforegetResuns(sunsu,l,array,remembergetlocation):

    if l in remembergetlocation:# 순서재조정할 k가 맞다면

        m= remembergetlocation.index(l)
        # print(array[m][0]+array[m][1])
        my_list=array[m][0]+array[m][1]
        if len(my_list) != len(set(my_list)): #중복여부 체크
            print('순서중에 중복이 존재.', [item for item in set(my_list) if my_list.count(item) > 1])
        else:
            pass

        newsunsu = array[m][0] +[x for x in sunsu if x not in array[m][0]+array[m][1] ] +array[m][1] #리스트 중복없애고 앞뒤로 붙히기

        return newsunsu

    else: #아니면 그대로 출력
        return sunsu


def makecorrestdongsu(list):
    for i in range(len(list)):
        if isinstance(list[i], int): #ex. 숫자7
            list[i]= str(100+list[i])
        else:
            pass

    return list


def calculate_weeks_since_start(reference_date, target_date):
    # 년도와 주차 계산
    reference_year, reference_week, _ = reference_date.isocalendar()
    target_year, target_week, _ = target_date.isocalendar()

    weeks_since_start = (target_year - reference_year) * 52 + target_week - reference_week

    return weeks_since_start

def remove_question_and_exclamation(text, status,misu):
    result = ""
    # print(text)
    if status != "배달" and '?' in text:  # 수거일 때
        # print(text)
        text = text.replace("?", "")
    elif status != "배달" and '!' in text:  # 수거일 때
        text = ""

    elif status != "수거" and '@' in text and misu == 0:  # 배달이면서 선불일때 미수표기 필요없음.
        text=""
    elif status != "수거" and '@' in text and misu != 0:  # 배달이면서 선불 아니면 미수표기
        text = text.replace("@", "")
    elif status != "배달" and '@' in text :  # 수거일때는 당연히 미수표기 필요 없음.
        text=""

    elif status != "수거" and '!' in text:  # 배달일 때
        text = text.replace("!", "")
    elif status != "수거" and '?' in text:  # 배달일 때
        text =""

    result += text
    # print(result)
    return result

def process_and_join_strings(text, status,misu):
    parts = text.split(',')
    cleaned_parts = [remove_question_and_exclamation(part, status,misu) for part in parts if remove_question_and_exclamation(part, status,misu)!=""]
    return ','.join(cleaned_parts)


def dividedf(df,munja):

    dfs_by_date = {date: group for date, group in df.groupby(df[munja].dt.date)}
    # 각 날짜별 데이터프레임 확인
    # for date, df_date in dfs_by_date.items():
        # print(f"Date: {date}")
        # print(df_date)
        # print()

    return dfs_by_date

if __name__ =="__main__":
    #주소 특이사항에 전화있는 사람 목록 뽑는 코드
    df =getdf3()
    df[df['전화여부']==True]['고객명'].to_csv('junha.txt',index=False)
    # print(df)