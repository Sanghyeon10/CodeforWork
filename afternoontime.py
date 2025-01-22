import datetime
hour =0
minute = 0


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

sunsucheck = False # False면 오름차순, True면 내림차순
# sunsucheck = True

#Flase면 기본, True일때만 접수 목록 리스트 강제로 적용하기
jubsulist= False
# jubsulist= True