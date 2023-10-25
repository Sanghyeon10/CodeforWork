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
# switch=True


today= datetime.datetime.now().date()
hour = 12+1
minute = 27
if (hour ==0 and minute==0) or time.weekday()==5 : #토요일이면 array형태로 표시해주는게 좋음.
    aftersigan = datetime.datetime(2023, 1, 1)
else:
    aftersigan= datetime.datetime.combine(today,datetime.datetime.strptime(f'{hour}:{minute}', "%H:%M").time())

# print(aftersigan)
sigandf= copy.deepcopy(df[df['등록일자']>aftersigan])




Sixfirst=[10,3,2,5,8]
Sixafter=[12,11,9]

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


item_count,gita_count, shoe_count , bedding_count,diffnumber , susun_count,long_count,  price_sum = supportmain.getdf4()



# 미리예약여부로 중복 일일이 확인 x하기
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

BB=''
AA=''
CC=''
tempnumber=""
tagnumber=""
#택번호와 개수 표시?



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
    # print(globals()['get'+str(l)],l)

    resunsu = supportmain.BeforegetResuns(sunsu,l,arrayforsunsu,remembergetlocation)
    # print(resunsu,l)
    for j in range(len(resunsu)):
        for i in range(len(globals()['get'+str(l)])):

            if globals()['get'+str(l)][i][3] == resunsu[j]: #동호수를꺼내서 15동부터 해당되는거 꺼내기

                if switch == True:#정해진 시간대라면,
                    for p in range(len(df2)) :#옷장에 있는거 택번호 가져올 정보
                        if df2.loc[df2.index[p],'고객명'] == globals()['get'+str(l)][i][1]: #맞는 택번호 구하기
                            tagnumber= df2.loc[df2.index[p],'택번호']
                            tempnumber=  str(item_count[df2.loc[df2.index[p],'고객명']])+'('+str(gita_count[df2.loc[df2.index[p],'고객명']])+')'
                            break #택첫번째면 충분함


                if dict.get((globals()['get'+str(l)][i][1]), 'a')!= "a": #비번이 있으면 4자리 숫자를 얻고 아니면 a를 얻음 a가 아니다= 비번있다,
                    if (globals()['get' + str(l)][i][2][-2:]) != '10': #10분이면 문앞이라 필요없음
                        AA =AA+"*"


                if (globals()['get'+str(l)][i][2][-2:])=='10': # 무슨k, 튜플중 첫번째 정보, 그안에 있는 시간관련정보 중 miniute정보 가져오기
                    tem=(globals()['get'+str(l)][i][1])#동호수 입력
                    AA = AA + (dict.get(tem,'문앞'))

                if (globals()['get'+str(l)][i][2][-2:])=='50':
                    AA= AA + '늦지말기'


                # print(globals()['get'+str(l)][i][0][0]) #배달 수거 들어있는 정보
                # print(shoe_count[globals()['get'+str(l)][i][0][1]]) #동호수를 넣어서 기타 개수 알아내기
                if globals()['get'+str(l)][i][0] != '수거' and globals()['get'+str(l)][i][1] in gita_count.keys() : #배달,수거배달이면서 재고가 0개라도 표시가능한 경우에
                    if int(shoe_count[globals()['get'+str(l)][i][1]])>0:#  운동화개수가 0 이상이면
                        AA = AA + '운동화'+str(shoe_count[globals()['get'+str(l)][i][1]])

                    if int(bedding_count[globals()['get'+str(l)][i][1]]) >0 : # 이불개수가 0이상이면
                        #재고자산과 운동화 개수가 다르면서 운동화 개수가 0이 아니라면
                        AA = AA + '이불' + str(bedding_count[globals()['get' + str(l)][i][1]])

                    if int(item_count[globals()['get'+str(l)][i][1]]) > int(gita_count[globals()['get'+str(l)][i][1]]) and int(gita_count[globals()['get'+str(l)][i][1]])>0 :
                        #기타 개수가 있고 재고자산보다 모자르면, 도 추가해주기
                        AA= AA + '도'



                if text.get(globals()['get'+str(l)][i][1],'a')!='a' : #주어진 동호수를 꺼냈는데 체크포인트에 내용이 있다면
                    if text.get(globals()['get'+str(l)][i][1],'a').count('?')>=1 : #물음표가 1개 이상이고
                        if globals()['get'+str(l)][i][0] != '배달':  #수거라면,(수거, 배달, 수거배달 중 배달만 아님)
                            AA = AA + text.get(globals()['get' + str(l)][i][1], '')
                        else: #배달이면 신발 줄수도 있다는뜻.
                            AA = AA +"+" #신발 잘 주는집이라는 표시.
                    else:
                        AA=AA+" "+ text.get(globals()['get'+str(l)][i][1],'')

                if globals()['get'+str(l)][i][1] in price_sum.keys(): #접수 금액 표시 가능하다면(=완성재고가 있다)
                    if (df3.loc[globals()['get'+str(l)][i][1],'총미수금'])>0: #미수금이 있다면,

                        if (df3.loc[globals()['get' + str(l)][i][1],'체류'] == item_count[globals()['get' + str(l)][i][1]])and (price_sum[globals()['get' + str(l)][i][1]] !=df3.loc[globals()['get' + str(l)][i][1],'총미수금']) :# 재고 체류 개수가 같은데도
                            AA = AA + " 진"+str(df3.loc[globals()['get' + str(l)][i][1],'총미수금'])

                        else:
                            AA = AA + " "+ str(price_sum[globals()['get' + str(l)][i][1]]) #빈칸하나 넣고 가격 표시

                        if (globals()['get' + str(l)][i][2][-2:]) == '10': #만일 문앞에 두는건데 선불이 아니면 미수인지 체크
                            AA = AA +" 미수?"

                    else: #총미수금이 0이면,선불이므로 개수와 선불표시하기
                        AA = AA + " "+ str(item_count[globals()['get' + str(l)][i][1]])+"선불"


                if globals()['get'+str(l)][i][1] not in price_sum.keys() and df3.loc[globals()['get' + str(l)][i][1],'총미수금']>0:
                    #접수금액표시 불가능한데(완성재고는 없는데) 미수금만 있다면
                    AA= AA +" 미수금"+str(df3.loc[globals()['get' + str(l)][i][1],'총미수금'])+"?"





                if globals()['get' + str(l)][i][1] in item_count.keys(): # item 딕셔너리에 자료가 있을때,(수거이더라도 불연속잡아낼때 쓰기)
                    # print(globals()['get' + str(l)][i][1], diffnumber[globals()['get'+str(l)][i][1]])
                    if int(item_count[globals()['get'+str(l)][i][1]]) !=0: #재고가 1개 이상이면서
                        if int(item_count[globals()['get'+str(l)][i][1]]) != int(diffnumber[globals()['get'+str(l)][i][1]]) +1 : #재고개수 = 택차이의 합+1이면 연속된 번호임
                            AA = AA + ' 불'+str(item_count[globals()['get' + str(l)][i][1]])

                        if susun_count[globals()['get'+str(l)][i][1]] !=0: #수선이라고 적혀있는 것이 1개 이상이라면
                            AA = AA + " 수"+str(susun_count[globals()['get' + str(l)][i][1]])

                        if long_count[globals()['get'+str(l)][i][1]] !=0: #긴것이 1개 이상이면
                            AA = AA + " 긴" + str(long_count[globals()['get' + str(l)][i][1]])

                        if df3.loc[globals()['get'+str(l)][i][1],'체류'] != item_count[globals()['get'+str(l)][i][1]]:# 완성개수와 재고재수가 불일치하면
                            if df3.loc[globals()['get'+str(l)][i][1],'총미수금']>0: #그러면서 미수금이 있어야 의미가 있음. 0이면 다 선불
                                AA = AA + " 선?"

                        


                print(f"{globals()['get' + str(l)][i][:3]}{AA}", tagnumber, tempnumber)

                BB=''
                AA=''
                CC=''
                tagnumber =''
                tempnumber =""


                if (globals()['get'+str(l)][i][0]) =='수거배달': #2개합친거면
                    countingnumber = countingnumber +2
                else:
                    countingnumber= countingnumber+1


                # print(c)
                if globals()['get' + str(l)][i][1] in c : #중복1개당 1발언
                    print('중복존재')
                c.append(globals()['get' + str(l)][i][1]) #배달수거 + 동호수




                # print(l)
    print()



# print(sigandf)
# newlist = np.empty((0,3), str) #늦게 등록된거 택번호 재고개수 표시하기
newlist =[]
templist=[]
# print(sigandf)
sigandf['동호수'] = sigandf['동호수'].apply(lambda x: int(x) if x.isdigit() else 0) # ex. "105"를 숫자105로 바꿔줌

#['고객명','택번호','재고개수'])
for i in range(len(sigandf)):
    if sigandf.loc[sigandf.index[i],'고객명'] in item_count.keys() : #옷장에서 찾을수 있다면
        templist.append(sigandf.loc[sigandf.index[i], '고객명']) #찾을 사람 이름 추가
        for j in range(len(df2)):
            if df2.loc[df2.index[j],'고객명']== sigandf.loc[sigandf.index[i],'고객명'] :#찾고있는 고객명이 일치한다면,
                templist.append(df2.loc[df2.index[j],'택번호'])
                break
        if len(templist)!=2: #택번호 안찍힌경우임 
            templist.append("0번호부재")
        templist.append(str(item_count[sigandf.loc[sigandf.index[i], '고객명']]) + '(' + str(
            gita_count[sigandf.loc[sigandf.index[i], '고객명']]) + ')')

        templist.append(sigandf.loc[sigandf.index[i] , '동호수'])
        templist.append(int(sigandf.loc[sigandf.index[i] , '시']))
        templist.append(int(sigandf.loc[sigandf.index[i] , '분']))


        newlist.append(templist)
        # newlist= np.concatenate((newlist, np.array([templist])) , axis= 0)
        templist=[]

    else:#옷장에 없으면
        pass

#
# print(newlist)
if sunsucheck == True:
    newlist = sorted(newlist, key=lambda x: (x[4],x[5], -x[3]))
    #시, 분을 기준으로 정렬하고 남은건 동호수로 정렬
elif sunsucheck == False:
    newlist = sorted(newlist, key=lambda x: (x[4], x[5], x[3]))
else:
    print("error")


if newlist == []: #빈칸이면 슬라이싱에 문제생김
    newlist.append(['',"",""])
newlist = supportmain.remove_duplicates_preserve_order(newlist)
#중복 제거하기
# NumPy 배열로 변환
newlist = np.array(newlist, dtype=object)[:,:3] #슬라이싱해서 뒤에꺼 날리기

print(newlist)


dashboradprint, nonharington=supportmain.checkingtime(df2,price_sum,df3,item_count)
print(dashboradprint)
s1=set(df['고객명']) #오늘 배달리스트의 있는 고객명들
ss=set(lastSatdf.values.flatten().tolist()) #지난주 동수일치
sss=set(lastlastSatdf.values.flatten().tolist()) ##지지난주 동수일치
junhaToset= set(junhadf.values.flatten().tolist()) | set(nonharington) #전화배달중 금액큰 비입주도 포함
# print(calllist.drop_duplicates(subset='고객명').values.flatten().tolist())
calllisttoset = set(calllist.drop_duplicates(subset='고객명').values.flatten().tolist())#중복제거후 리스트화 , 지지난주 동수일치
fullllisttoset= set(fulllist.drop_duplicates(subset='고객명').values.flatten().tolist()) #지난주 풀 리스트

potentail_beadaldf=pd.read_csv('potential beadal.txt',sep=" ")
potentail_beadaldf= set(potentail_beadaldf.values.flatten())
# print(potentail_beadaldf.values.flatten())


allofalllistset= set(allofalllist.drop_duplicates(subset='고객명').values.flatten().tolist())


s2= set(df5) #미래예약 파일 집합화
# print(s2)

exceptset=set(["108-2504"] ) #전화 일시적 예외 적는칸
# print('exceptset',exceptset)

if s2 == set():#빈집합이면 예약 비포함
    A= "예약은 비포함"
else:
    A="후예약 포함되어있음"

if datetime.datetime.today().strftime("%A")=="Friday" and 12<nowhour  :
    fridayTodo='내일꺼 찾기'
else:
    fridayTodo = ''

#자기자신과 중복은 제외할것
print(A,"exceptset",exceptset, "비입주 메모",supportmain.GetNonharingtonMemo(text.get('비입주')))
print('지지난주이전 동수 일치', supportmain.getorderwithprice(price_sum,sss.difference(s1|s2|exceptset),df3,item_count ))
print('지지난주 것 전체 리스트', supportmain.getorderwithprice(price_sum,calllisttoset.difference(s1|s2|sss|exceptset),df3,item_count ))
print('지난주 동수 일치',supportmain.getorderwithprice(price_sum,ss.difference(s1|s2|calllisttoset|exceptset) ,df3,item_count))  # 지지난주껏도 중복제거할까?
print('지난주 것 전체 리스트', supportmain.getorderwithprice(price_sum, fullllisttoset.difference(s1|s2|calllisttoset|ss|exceptset) ,df3,item_count)) #지지난주것도 표현하면 너무 김.
print('잠재적 배달 리스트',supportmain.getorderwithprice(price_sum,potentail_beadaldf.difference(s1|s2|exceptset),df3,item_count ))
print('\033[1m\033[3m전화 배달 리스트', supportmain.getorderwithprice(price_sum,junhaToset.difference(s1|s2|exceptset) ,df3,item_count),"\033[0m")
# print('전체 리스트',supportmain.getorderwithprice(price_sum,allofalllistset.difference(s1|s2|exceptset|calllisttoset|fullllisttoset) ,df3,item_count))
print(countingnumber== len(df.index), len(df.index) , datetime.datetime.today().strftime("%A"),fridayTodo )


