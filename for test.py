from datetime import datetime, timedelta


def calculate_weeks_since_start(reference_date, target_date):
    # 년도와 주차 계산
    reference_year, reference_week, _ = reference_date.isocalendar()
    target_year, target_week, _ = target_date.isocalendar()

    weeks_since_start = (target_year - reference_year) * 52 + target_week - reference_week

    return weeks_since_start


# 특정일
specific_date = datetime(2024, 1, 2)  # 예시로 2024년 1월 15일로 설정

# 토요일을 기준으로 주차 계산
reference_date = datetime.now()  # 5는 토요일의 weekday 값
weeks_since_start = calculate_weeks_since_start( specific_date,reference_date)

print(f"{specific_date}로부터 {weeks_since_start} 주가 지났습니다.")
