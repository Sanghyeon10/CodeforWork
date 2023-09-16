import re
import datetime


def extract_dates_and_delta(input_string):

    # 문자열에서 8자리 연속된 숫자 추출
    date_strings = re.findall(r'\d{8}', input_string)

    # 현재 날짜 가져오기
    current_date = datetime.datetime.now()

    for date_str in date_strings:
        # 8자리 숫자를 날짜로 변환
        try:
            date = datetime.datetime.strptime(date_str, '%Y%m%d')

            # 현재 날짜와의 차이 계산
            delta = current_date - date

            # 결과 출력
            print(f"날짜 문자열: {date_str}")
            print(f"날짜: {date.strftime('%Y-%m-%d')}")
            print(f"Delta 시간: {delta}")

            # 입력 문자열에서 추출된 날짜 부분을 빈 문자열로 대체하여 출력
            input_string = input_string.replace(date_str, '')
        except ValueError:
            print(f"잘못된 날짜 형식: {date_str}")

    # 나머지 문자열 출력
    print("나머지 문자열:", input_string)


# 테스트 문자열
input_string = "오늘은 20230916 날짜입니다. "

# 함수 호출
extract_dates_and_delta(input_string)
