import pandas as pd
import datetime
import re
import copy
import supportmain



def printtingf(df, get_index, i, k):
    a = (df.loc[df.index[i], '수거/배달'], df.loc[df.index[i], '고객명'], df.loc[df.index[i], '요청일자'],df.loc[df.index[i], '동호수'] )
    get_index.append(df.index[i])
    globals()['get' + str(k)].append(a)

df= supportmain.getdf1()

noon=['09','10']
noon1=['11','12']
afternoon =['17','18','19','20']
early=['10']
sunsu=['115','114','113','112','111','110','109', '108', '107','106','105','104','103','102','101']

sunsu= sunsu[::-1] #조절하는 기능

switch=False # 개수와 택번호 표시 여부
time = datetime.datetime.now()
hour = time.hour
if hour<16 : #오후 12~4시라면 필요한기능
    switch=True
    # pass
# switch=True



plussunsu=[]
for o in range(len(df)): #문자이름 뽑아내기
    if df.loc[df.index[o],'문자이름'] == True:
        plussunsu.append(df.loc[df.index[o],'고객명'])

sunsu = plussunsu + sunsu #기존 순서문자열 앞에 추가해주기( 보통 가게라서 먼저가기 때문)
# print(sunsu)
# df= df[['순번', '등록일자', '요청일자', '수거/배달', '등록위치', '전화번호', '고객명', '주소', '상태', '수정']]


df2 = supportmain.getdf2()


## 지난주 토요일날까지 완성된것 리스트 중 오늘 배달갈곳의 동수가 일치되는지 구하는 것.
lastSatdf , lastlastSatdf= supportmain.getpastSat(df,df2)

#주소 특이사항에 전화라고 적힌 사람 리스트중 완성된게 있다면 표시
jusodf=pd.read_csv('juso.txt',sep=" ")
jusodf= jusodf[jusodf['고객명'].isin(df2['고객명'])]
# print(jusodf)


item_count, price_sum, shoe_count = supportmain.getdf4()



# df3 = pd.read_excel(r'C:\Users\user\Desktop\고객정보.xls')
# df3= df3[['고객명','체류']]
# df3= df3.dropna(axis=0)
# df3['고객명'] = df3['고객명'].apply(lambda x: x.split('\n')[0])





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



c=[] #중복체크용
countingnumber=0
dict={} # password 담는용
text={} # 체크 포인트 담는용
supportmain.findingpassword('data.txt',dict)
supportmain.findingpassword('checkpoint.txt',text)

BB=''
AA=''
CC=''
tempnumber=""
tagnumber=""
#택번호와 개수 표시?





for h in range(k+1): #배달 수거 합치기
    (globals()['get' + str(h)]) =supportmain.mergeforget(globals()['get' + str(h)])



for l in range(k+1): #모든 리스트 돌리기
    # print(globals()['get'+str(l)],l)
    for j in range(len(sunsu)):
        for i in range(len(globals()['get'+str(l)])):

            if globals()['get'+str(l)][i][3] == sunsu[j]: #동호수를꺼내서 15동부터 해당되는거 꺼내기

                if switch == True:#정해진 시간대라면,
                    for p in range(len(df2)) :#옷장에 있는거 택번호 가져올 정보
                        if df2.loc[df2.index[p],'고객명'] == globals()['get'+str(l)][i][1]: #맞는 택번호 구하기
                            tagnumber= df2.loc[df2.index[p],'택번호']
                            tempnumber=  str(item_count[df2.loc[df2.index[p],'고객명']])+'('+str(shoe_count[df2.loc[df2.index[p],'고객명']])+')'




                if (globals()['get'+str(l)][i][2][-2:])=='10': # 무슨k, 튜플중 첫번째 정보, 그안에 있는 시간관련정보 중 miniute정보 가져오기
                    tem=(globals()['get'+str(l)][i][1])#동호수 입력
                    AA = AA + (dict.get(tem,'문앞'))

                if (globals()['get'+str(l)][i][2][-2:])=='50':
                    AA= AA + '늦지말기'

                # print(shoe_count.keys())
                # print(globals()['get'+str(l)][i][0][0]) #배달 수거 들어있는 정보
                # print(shoe_count[globals()['get'+str(l)][i][0][1]]) #동호수를 넣어서 기타 개수 알아내기
                if globals()['get'+str(l)][i][0] == '배달' and globals()['get'+str(l)][i][1] in shoe_count.keys() : #배달이면서 재고가 0개라도 표시가능한 경우에
                    if int(item_count[globals()['get'+str(l)][i][1]]) == int(shoe_count[globals()['get'+str(l)][i][1]]):# 운동화개수 = 재고자산인경우,
                        AA = AA + '운동화'+str(shoe_count[globals()['get'+str(l)][i][1]])

                    elif int(item_count[globals()['get'+str(l)][i][1]]) != int(shoe_count[globals()['get'+str(l)][i][1]]) and int(shoe_count[globals()['get'+str(l)][i][1]]) !=0:
                        #재고자산과 운동화 개수가 다르면서 운동화 개수가 0이 아니라면
                        AA = AA + '운동화' + str(shoe_count[globals()['get' + str(l)][i][1]]) + '도'

                    else: #재고 자산과 운동화개수가 다르면서 운동화개수가 0인경우 즉 운동화 없음.
                        pass



                if text.get(globals()['get'+str(l)][i][1],'a')!='a' : #주어진 동호수를 꺼냈는데 체크포인트에 내용이 있다면
                    AA=AA+ text.get(globals()['get'+str(l)][i][1],'')

                if globals()['get'+str(l)][i][1] in price_sum.keys(): #접수 금액 표시 가능하다면
                    AA = AA+ " "+ str(price_sum[globals()['get' + str(l)][i][1]]) #빈칸하나 넣고 가격 표시


                print(globals()['get'+str(l)][i][:-1] ,AA, tagnumber,tempnumber )

                BB=''
                AA=''
                CC=''
                tagnumber =''
                tempnumber =""


                if (globals()['get'+str(l)][i][0]) =='수거배달': #2개합친거면
                    countingnumber = countingnumber +2
                else:
                    countingnumber= countingnumber+1


                # if (globals()['get'+str(l)][i][1]=='110-1504'):
                #     print('호출금지')

                # print(c)
                if globals()['get' + str(l)][i][1] in c : #중복1개당 1발언
                    print('중복존재')
                c.append(globals()['get' + str(l)][i][1]) #배달수거 + 동호수




                # print(l)
    print()
print(supportmain.checkingtime(df2,price_sum))
print(supportmain.checkingtime(df2,price_sum))
s=set(df['고객명'])
ss=set(lastSatdf.values.flatten().tolist())
sss=set(lastlastSatdf.values.flatten().tolist())
#자기자신은 제외할것

print('지지난주이전 혹시 예약?',sss-s)
print( '예약잡혀있을수도',ss-s)
print('전화할것', jusodf.values.flatten().tolist())
print(countingnumber== len(df.index), len(df.index))
