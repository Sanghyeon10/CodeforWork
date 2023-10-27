import datetime
hour = 12+2
minute = 7



Sixfirst=[11]
Sixafter=[]

sevenfirst=[]
sevenafter=[]

sevenhalffirst=[]
sevenhalfafter=[]

eightfirst=[]
eightafter=[]



tenfirst=[]
tenafter=[3]

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