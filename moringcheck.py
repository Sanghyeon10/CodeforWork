import pandas as pd
import datetime
import re
import copy
import supportmain
import numpy as np


def printtingf(df, get_index, i, k):
    a = (df.loc[df.index[i], '수거/배달'], df.loc[df.index[i], '고객명'], df.loc[df.index[i], '요청일자'],df.loc[df.index[i], '동호수'], supportmain.lastpiece(df.loc[df.index[i], '고객명']) )
    get_index.append(df.index[i])
    globals()['get' + str(k)].append(a)


df= supportmain.getdf1()


afternoon =['17','18','19','20']
sunsu=['115','114','113','112','111','110','109', '108', '107','106','105','104','103','102','101']

sunsucheck = False # False면 오름차순, True면 내림차순
# sunsucheck = True
#조절하는 기능
sunsu = sorted(sunsu, reverse=sunsucheck)
# print(sunsu)

switch=False # 개수와 택번호 표시 여부
time = datetime.datetime.now()
nowhour = time.hour
if nowhour<16 : #오후 12~4시라면 필요한기능
        if time.weekday()!=5:
            switch=True
        else:
            pass
    # pass
switch=True


today= datetime.datetime.now().date()
hour = 0
minute = 0
if (hour ==0 and minute==0) or time.weekday()==5 : #토요일이면 array형태로 표시해주는게 좋음.
    aftersigan = datetime.datetime(2023, 1, 1)
else:
    aftersigan= datetime.datetime.combine(today,datetime.datetime.strptime(f'{hour}:{minute}', "%H:%M").time())

# print(aftersigan)
sigandf= copy.deepcopy(df[df['등록일자']>aftersigan])




Sixfirst=[]
Sixafter=[]

sevenfirst=[]
sevenafter=[]

sevenhalffirst=[]
sevenhalfafter=[]

eightfirst=[]
eightafter=[]





tenfirst=[]
tenafter=[]

elevenfirst=[]
elevenafter=[]

elevenhalffirst=[]
elevenhalfafter=[]

twelvefirst=[]
twelveafter=[]





Sixfirst=supportmain.makecorrestdongsu(Sixfirst)
Sixafter=supportmain.makecorrestdongsu(Sixafter)
sevenfirst=supportmain.makecorrestdongsu(sevenfirst)
sevenafter=supportmain.makecorrestdongsu(sevenafter)
sevenhalffirst=supportmain.makecorrestdongsu(sevenhalffirst)
sevenhalfafter=supportmain.makecorrestdongsu(sevenhalfafter)
eightfirst=supportmain.makecorrestdongsu(eightfirst)
eightafter=supportmain.makecorrestdongsu(eightafter)

tenfirst=supportmain.makecorrestdongsu(tenfirst)
tenafter=supportmain.makecorrestdongsu(tenafter)
elevenfirst=supportmain.makecorrestdongsu(elevenfirst)
elevenafter=supportmain.makecorrestdongsu(elevenafter)
elevenhalffirst=supportmain.makecorrestdongsu(elevenhalffirst)
elevenhalfafter=supportmain.makecorrestdongsu(elevenhalfafter)
twelvefirst=supportmain.makecorrestdongsu(twelvefirst)
twelveafter=supportmain.makecorrestdongsu(twelveafter)




arrayforsunsu= [[tenfirst,tenafter], [elevenfirst,elevenafter], [elevenhalffirst,elevenhalfafter],[twelvefirst, twelveafter], [Sixfirst,Sixafter], [sevenfirst,sevenafter], [sevenhalffirst,sevenhalfafter], [eightfirst,eightafter] ]











plussunsu=[]
for o in range(len(df)): #문자이름 뽑아내기
    if df.loc[df.index[o],'문자이름'] == True:
        plussunsu.append(df.loc[df.index[o],'고객명'])

sunsu = plussunsu + sunsu #기존 순서문자열 앞에 추가해주기( 보통 가게라서 먼저가기 때문)
# print(sunsu)


df2 = supportmain.getdf2()
df2 = df2.sort_values(by='날짜차이', ascending=True).drop_duplicates(subset='고객명', keep='first').sort_values(by='접수일자', ascending=True)  # 가장 최신 완성일만 남기기

# print(df2)

## 지난주 토요일날까지 완성된것 리스트 중 오늘 배달갈곳의 동수가 일치되는지 구하는 것.
lastSatdf , lastlastSatdf, calllist , fulllist ,allofalllist = supportmain.getpastSat(df,df2)

#주소 특이사항에 전화라고 적힌 사람 리스트중 완성된게 있다면 표시
junhadf=pd.read_csv('junha.txt',sep=" ")
junhadf= junhadf[junhadf['고객명'].isin(df2['고객명'])]
# print(junhadf)


item_count,gita_count, shoe_count , bedding_count,diffnumber , susun_count,long_count,  price_sum ,shoulcheck_count= supportmain.getdf4()



# 접수리스트로 활용하기
df5 = supportmain.getdf5()


remembergetlocation=[]
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

remembergetlocation.append(k)

k= k+1

for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] == '11' and df.loc[df.index[i],'분']!='30' : #11시
        if df.index[i] not in get_index :
            #오전 걸러내기

            printtingf(df, get_index, i, k)

remembergetlocation.append(k)


k= k+1

for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] == '11' and df.loc[df.index[i],'분']=='30'  : #11시 30분
        if df.index[i] not in get_index :
            #오전 걸러내기

            printtingf(df, get_index, i, k)

remembergetlocation.append(k)



k= k+1

for i in range(len(df)):
    if df.loc[df.index[i],'요청일자'][0:2] == '12': #12시
        if df.index[i] not in get_index :
            #오전 걸러내기

            printtingf(df, get_index, i, k)



remembergetlocation.append(k)


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

remembergetlocation.append(k)

k = k+1

for i in range(len(df)):
    if df.loc[df.index[i], '요청일자'][0:2] in afternoon:
        if df.loc[df.index[i],'시']=='19' and df.loc[df.index[i],'분']!='30' and df.index[i] not in get_index:
            printtingf(df, get_index, i, k)

remembergetlocation.append(k)

k = k+1

for i in range(len(df)):
    if df.loc[df.index[i], '요청일자'][0:2] in afternoon:
        if df.loc[df.index[i],'시']=='19' and df.loc[df.index[i],'분']=='30'  and df.index[i] not in get_index:
            printtingf(df, get_index, i, k)

remembergetlocation.append(k)

k = k+1

for i in range(len(df)):
    if df.loc[df.index[i], '요청일자'][0:2] in afternoon:
        if df.loc[df.index[i],'시']=='20' and df.loc[df.index[i],'분']=='00'  and df.index[i] not in get_index:
            printtingf(df, get_index, i, k)

remembergetlocation.append(k)


k = k+1


for i in range(len(df)): #남은게 있다면 출력 (잘못된 시간대일경우 대비)
    if  df.index[i] not in get_index:
        printtingf(df, get_index, i, k)




c=[] #중복체크용
countingnumber=0
dict={} # password 담는용
text={} # 체크 포인트 담는용
supportmain.findingpassword('data.txt',dict)
supportmain.findingpassword('checkpoint.txt',text)

BB=[]
AA=''
CC=[]
tempnumber=""
tagnumber=""
#택번호와 개수 표시?
gettotalnumber=0


#총미수금 알아낼 정보 얻기
df3= supportmain.getdf3()
df3.set_index('고객명', inplace= True)
df3=df3[["총미수금","체류"]]

# print(df3.loc['111-2005',"체류"])


for h in range(k+1): #배달 수거 합치기 + 끝호수 1~5 정렬해주기
    (globals()['get' + str(h)]) =supportmain.mergeforget(globals()['get' + str(h)])
    globals()['get' + str(h)].sort(key=lambda x: x[-1], reverse=False) #마지막꺼에 1~5들어있으므로 이것을 기준으로 정렬해주기
    # print((globals()['get' + str(h)]))


for l in range(k+1): #모든 리스트 돌리기
    # print((globals()['get'+str(l)]),l)
    gettotalnumber= gettotalnumber + len(globals()['get'+str(l)])

    resunsu = supportmain.BeforegetResuns(sunsu,l,arrayforsunsu,remembergetlocation)
    # print(resunsu,l)
    for j in range(len(resunsu)):
        for i in range(len(globals()['get'+str(l)])):

            if globals()['get'+str(l)][i][3] == resunsu[j]: #동호수를꺼내서 15동부터 해당되는거 꺼내기

                # print(globals()['get'+str(l)][i][0][0]) #배달 수거 들어있는 정보
                # print(shoe_count[globals()['get'+str(l)][i][0][1]]) #동호수를 넣어서 기타 개수 알아내기



                if df3.loc[globals()['get' + str(l)][i][1],'체류']!=0:
                    AA = " 체류"+str(df3.loc[globals()['get' + str(l)][i][1],'체류'])
                    BB.append(globals()['get' + str(l)][i][1])

                else:
                    AA = AA+ "    "

                if df3.loc[globals()['get' + str(l)][i][1],'총미수금']!=0:
                    AA = AA+ " 총미수금" +str(df3.loc[globals()['get' + str(l)][i][1],'총미수금'])
                    if df3.loc[globals()['get' + str(l)][i][1],'체류']==0:
                        #체류가 0인데 미수가 있으면 명백한 미수의 경우의수
                        CC.append(globals()['get' + str(l)][i][1])

                else:
                    AA =AA+ "              "

                if globals()['get'+str(l)][i][1] in price_sum.keys():
                    AA =AA+ " 재고에는" +str(price_sum[globals()['get' + str(l)][i][1]]) +"("+str(item_count[globals()['get' + str(l)][i][1]])+ ")"
                    #
                    # if int(shoe_count[globals()['get'+str(l)][i][1]])>0:#  운동화개수가 0 이상이면
                    #     AA = AA + '운동화'+str(shoe_count[globals()['get'+str(l)][i][1]])



                if globals()['get' + str(l)][i][0]=='배달'and df3.loc[globals()['get' + str(l)][i][1],'총미수금']==0 and df3.loc[globals()['get' + str(l)][i][1],'체류']==0:
                    #배달이면서, 미수금이0이면 의미없어서 프린트 안함
                    pass
                else:
                    print(f"{globals()['get' + str(l)][i][:3]}{AA}")

                AA=''
                tagnumber =''
                tempnumber =""


                # print(c ,globals()['get' + str(l)][i][1] )
                if globals()['get' + str(l)][i][1] in c : #중복1개당 1발언
                    pass # 중복존재여부 체크하더라도 바로 밑에 안나와서 큰 의미 없음.

                # print(c)
                c.append(globals()['get' + str(l)][i][1]) #배달수거 + 동호수


                # print(l)
                for m in range(len(df5)):

                    # print(globals()['get' + str(l)][i][1], df5.loc[df5.index[m],'고객명'])
                    if globals()['get' + str(l)][i][1] == df5.loc[df5.index[m], '고객명']:
                        print(df5.loc[df5.index[m], '고객명'], df5.loc[df5.index[m], '상품명'])


                print()
    print()



print("체류",len(BB),BB, "미수",len(CC),CC)
print('전체개수',gettotalnumber)
