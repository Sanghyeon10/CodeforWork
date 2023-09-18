import re
import datetime

def ReplaceDatesWithDateDifferences(input_string):
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
                input_string = input_string.replace(date_str, f'{delta.days} days ago')

            except ValueError:
                # 날짜 형식이 잘못된 경우 무시
                pass

    except Exception as e:
        # 예외 처리 (원하는 방식으로 처리)
        print(f"에러 발생: {str(e)}")

    return input_string

# 테스트
input_string = "This is a sample string with a datand another date 200001014."
result = ReplaceDatesWithDateDifferences(input_string)
print(result)
