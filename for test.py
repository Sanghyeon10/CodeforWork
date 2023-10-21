input_string = "4-1 홍길동 김철수 김영희 나도현 ///김영희 아픔."

# 결과를 저장할 딕셔너리들
students_dict = {}
miscellaneous_dict = {}


# "///"을 포함하는지 확인
if "///" in input_string:
    # 딕셔너리를 생성 (///이 있는 경우)
    split_string= input_string.split("///")[0]
    split_string=split_string.split()
    class_name = split_string[0]
    student_names = split_string[1:]
    students_dict[class_name] = student_names

    miscellaneous_dict[class_name] = input_string.split("///")[1]

else:
    split_string=input_string.split()
    # 딕셔너리를 생성 (///이 없는 경우)
    class_name = split_string[0]
    student_names = split_string[1:]

    students_dict[class_name] = student_names
    miscellaneous_dict[class_name] = ""  # 기타사항이 없는 경우 None으로 처리

# 결과 출력
print("학생 딕셔너리:", students_dict)
print("기타사항 딕셔너리:", miscellaneous_dict)
