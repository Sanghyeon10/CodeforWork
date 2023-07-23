import os
from datetime import datetime, timedelta

def read_text_files_for_week():
    big =0
    # Get the current date
    today = datetime.now().date()

    # Generate a list of dates for the past 7 days
    dates_for_week = [today - timedelta(days=7)+ timedelta(days=i) for i in range(7)]

    # Convert each date to a string in the format 'YYYY-MM-DD'
    date_strings = [date.strftime('%Y-%m-%d') for date in dates_for_week]

    # File path to the directory containing the text files
    file_directory = ''

    for date_string in date_strings:
        file_path = os.path.join(file_directory, f'{date_string} 일기.md')

        if os.path.exists(file_path):
            print(f"Reading file: {file_path}")
            with open(file_path, 'r', encoding='utf-8' ) as f:
                lines = f.readlines()

                check=False #이전칸이 빈칸이면 True 아니면 False
                k=0
                for line in lines:
                    # print(line)
                    if line =="\n" and check==False:#빈칸인데다가 연속빈칸아니면
                        k +=1
                        check=False
                    elif line =="\n" and check==True: # 빈칸인데 연속빈칸이면 pass
                        pass
                    else:
                        if line in "오늘 있었던 일":#이 아래는 의미없어서 break
                            break
                        if "get{}".format(k) not in globals():
                            globals()["get{}".format(k)] = []

                        globals()["get{}".format(k)].append(line)
                        check == False
                        # print( globals()["get{}".format(k)])


                    # print(line,'ee')
                    # print(line.strip())
                print()
                big= max(big,k)


        else:
            print(f"File not found for date: {date_string}")
            print()
# Call the function to read text files for the past week
    return big

from collections import OrderedDict

def remove_duplicates_with_order(input_list):
    return list(OrderedDict.fromkeys(input_list))

def remove_duplicates_except_specified(input_list):

    result_list = []
    jongbocklist=[]

    for element in input_list:
        if "O" in element or "X" in element  : #보존해야하는 요소가 있다면 일단 추가
            result_list.append(element.rstrip("\n"))

        elif element in jongbocklist: #보존요소도 아니고 중복도 아니면 추가
            pass
        else: #보존요소가 아니고 중복이면 pass
            result_list.append(element.rstrip("\n"))
            jongbocklist.append(element)


    return result_list




number = read_text_files_for_week()


exceptlist="OX"
print()
i=0
while i<number:
    if "get{}".format(i) in globals(): #변수가 있으면 진행
        globals()["get{}".format(i)] = remove_duplicates_except_specified(globals()["get{}".format(i)])
        # globals()["get{}".format(i)] =remove_duplicates_with_order(globals()["get{}".format(i)])
        print(globals()["get{}".format(i)])
    i +=1