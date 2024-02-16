from datetime import datetime, timedelta


def remove_question_and_exclamation(text, status):
    result = ""

    if status != "배달" and '?' in text:  # 수거일 때
        text = text.replace("?", "")
    elif status != "수거" and '!' in text:  # 배달일 때
        text = text.replace("!", "")

    result += text
    return result

def process_and_join_strings(text, status):
    parts = text.split(',')
    cleaned_parts = [remove_question_and_exclamation(part, status) for part in parts]
    return ','.join(cleaned_parts)

# 테스트
input_string = "안녕하세요!, 오늘!은! 어떤 날씨인가요? 좋은 하루 되세요!"
output_string = process_and_join_strings(input_string, "수거")
print(output_string)
