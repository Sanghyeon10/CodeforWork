import pandas as pd
import datetime
import re
import supportmain



isprintcheck=pd.Series(dtype='object')
#데이터 프레임 만들것이라면 input 출력
with open('checkpoint.txt', 'r', encoding='utf-8') as f: #010전화번호 csv로 출력하는 코드
    for line in f:
        if "010-" in line:
            isprintcheck= pd.concat([isprintcheck, pd.Series(line.rstrip("\n"))])

if len(isprintcheck)!=0:# 출력할게 있다면
    input("0.0번칸 확인 1.후예약 확인 2.물건확인과 메모확인")



now = datetime.datetime.now() #+ datetime.timedelta(days=3)
print('오늘날짜',now)

print('배달리스트 토요일까지 껄로 했나?')
day=2 # 월요일에서 토요일로 2일뒤로
week = now.weekday()+day
pastSat= now - datetime.timedelta(days= (week) ,hours= now.hour-23)
print(pastSat)



df= supportmain.getdf2() #옷장조회
# df= df[['접수일자','완성일자', '고객명','옷장번호']]
df['몇주째']= df['완성일자'].apply(lambda x: x.strftime("%U"))
df = df.sort_values(by='날짜차이', ascending=True).drop_duplicates(subset='고객명', keep='first').sort_values(by='접수일자', ascending=True)  # 가장 최신 완성일만 남기기
# print(df)
#비입주 조절용 현재는 큰 의미없음
df=df[df['비입주']=='입주민']
df=df[df['완성일자']<=pastSat] #앞에서 최신 완성일과 오늘날자의 차이를 구하고, 최신완성일 기준으로 중복을 제거하므로,
#최근 완성날짜거가 지난주 토요일까지 완성되야지 살아남음.

# print(df)


#전화번호,전화여부 뽑기
dff= supportmain.getdf3()


####

#배달 리스트 가져오기
df2= pd.read_excel(r'C:\Users\user\Desktop\수거배달.xls')
df2 = df2[['수거/배달','고객명']]
df2['고객명'] = df2['고객명'].apply(lambda x: x.split(' ')[-1])
df2= df2[df2['수거/배달']=='배달'] #배달만 살리고 수거는 없애기.
df2=df2['고객명']
df2= df2.tolist()

# print(df2)
# 후예약 가져오기
df5= supportmain.getdf5()

baedallist= df5 + df2
# print(baedallist)


#count 구하기
item_count,gita_count, shoe_count , bedding_count,diffnumber , susun_count,long_count,  price_sum= supportmain.getdf4()



#기타사항 가져오기
dictt={}
gita= supportmain.findingpassword('gita.txt',dictt)


numberlist=[]
remaining=0 #남아있는거 세는 변수
jungbokcheck=[]
BB=''
CC=''
gijun=df.loc[df.index[0],'몇주째']
tempremaining=""

junhadf=pd.read_csv('junha.txt',sep=" ").values.flatten()#.tolist()


# print(df)
for i in range(len(df)):#중복이 제거된 df라 그냥 돌리면됨.
    #전화여부와 불연속 여부도 표현할 이유가 없음.
    # print(df.loc[dff.index[i],'고객명'],df.loc[df.index[i],'날짜차이'].days)
    number=df.index[i] #오류방지용 순서넣기
    juchacounting= supportmain.calculate_weeks_since_start(datetime.datetime.now(), df.loc[df.index[i], '완성일자']  )
    if i==0:
        print(juchacounting)


    if df.loc[df.index[i],'몇주째']== gijun:
        pass
    else:
        gijun = df.loc[df.index[i], '몇주째'] #기준 업
        print(juchacounting)#\n누르기+주차표시
        # print(df.loc[:, '몇주째'])

    for j in range(len(dff)): #dff고객정보 의미
        if dff.loc[dff.index[j],'고객명'] == df.loc[df.index[i],'고객명']: #찾는것을 찾으면 정보 붙히기
            number = dff.loc[dff.index[j],'휴대폰']
            if dff.loc[dff.index[j],'체류']!=item_count[dff.loc[dff.index[j],'고객명']]:
                tempremaining='불일치'
            else:
                tempremaining=""

            remainings = str(dff.loc[dff.index[j],'체류'])+','+str(item_count[dff.loc[dff.index[j],'고객명']])+'('+str(gita_count[dff.loc[dff.index[j],'고객명']]) + ')'+tempremaining
            totalremaining = int(dff.loc[dff.index[j],'체류'])
            inventories= int(item_count[dff.loc[dff.index[j],'고객명']])
            # print(dff.loc[dff.index[j],'체류']==item_count[dff.loc[dff.index[j],'고객명']])


            if (df.loc[df.index[i],'고객명']) in baedallist : # (df2.loc[df2.index[l],'고객명']): #찾는게 있다면, df2에는 배달만 살려놓아서 명단에 있으면 배달임.
                CC='배달리스트'

            # print(junhadf)
            if (df.loc[df.index[i],'고객명']) in junhadf:
                CC= CC+ "전화"

            if long_count[df.loc[df.index[i],'고객명']]>0: #코트 원피스같은게 있으면
                CC= CC+ "긴"+str(long_count[df.loc[df.index[i],'고객명']])

            # print(int(bedding_count[dff.loc[dff.index[j],'고객명']]))

            if int(bedding_count[dff.loc[dff.index[j],'고객명']])>0: #이불이 있으면 그건 따로 글자로 표현
                BB= BB+"이불"+str(bedding_count[dff.loc[dff.index[j],'고객명']])

            if dictt.get(dff.loc[dff.index[j],'고객명'],'a')!='a' : #주어진 고객명을 검색했는데 기타텍본에 내용이 있다면
                BB= BB + dictt.get(dff.loc[dff.index[j],'고객명'],'a')

        else:
            pass
    #number 값 획득

    print(df.loc[df.index[i], '고객명'], number,remainings ,df.loc[df.index[i], '날짜차이'].days ,BB,CC)



    numberlist.append((number,totalremaining,inventories,df.loc[df.index[i], '고객명'],juchacounting))
    # if df.loc[df.index[i],'고객명'] == '107-1304':
    #     print('평일 늦은 저녁에나 가능')

    jungbokcheck.append(df.loc[df.index[i],'고객명'])
    number= 'end' #number 초기화
    remaining = 0
    totalremainings = ''
    inventories=""
    CC=""
    BB=''



print()
print()


jungbokcheck=[]
forprintdf=pd.Series(dtype='object')
notpirnt=[] #출력하지 않을 동호수
notpirnt= notpirnt+baedallist
print(notpirnt)


# print(numberlist)
B = -int(input('전화 번호 리스트 출력기준 주차 - 역전'))

for i in range(len(numberlist)):
    if numberlist[i][3] not in notpirnt and numberlist[i][4]<=B:
        print(numberlist[i][0])
        print()


# if B=='0':
#     pass
#
#
# elif B=='1':
#     for i in range(len(numberlist)):
#         if numberlist[i][1]==1 and numberlist[i][3] not in notpirnt:
#             print(numberlist[i][0])
#             print()
#
#
# elif B=='2':
#     for i in range(len(numberlist)):
#         if numberlist[i][1]>=2 and numberlist[i][3] not in notpirnt :
#             print(numberlist[i][0])
#             print()
#
#
# else:
#     for i in range(len(numberlist)):
#         if numberlist[i][3] not in notpirnt:
#             print(numberlist[i][0])
#             print()



with open('checkpoint.txt', 'r', encoding='utf-8') as f: #010전화번호 csv로 출력하는 코드
    for line in f:
        if "010-" in line:
            forprintdf= pd.concat([forprintdf, pd.Series(line.rstrip("\n"))])



# forprintdf =pd.DataFrame(forprintdf,columns=['전화번호'])
forprintdf.name='전화번호'
print(forprintdf)
print(len(forprintdf))
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