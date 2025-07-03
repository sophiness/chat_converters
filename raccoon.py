import re

def raccoon_converter(text):
    """텍스트를 너굴체로 변환하는 함수"""
    if not text or not isinstance(text, str):
        return text
    
    result = text

    # 0. 작은따옴표 안의 내용 보호
    quoted_parts = {}
    quote_pattern = r"'([^']*?)'"
    
    def replace_quoted(match):
        placeholder = f"TEMP_QUOTE_{len(quoted_parts)}"
        quoted_parts[placeholder] = match.group(0)
        return placeholder
    
    result = re.sub(quote_pattern, replace_quoted, result)
    
    # 1. "아아" 보호 (아이스아메리카노, 의성어)
    result = re.sub(r'아아', 'TEMP_AA', result)
    
    # 2. "안녕" → "굴하" 변환
    result = re.sub(r'안녕', '구리구리안녕구리', result)
    # 3. "하이" → "냥하" 변환 (새로 추가)
    result = re.sub(r'하이', '구리구리하이구리', result)
    result = re.sub(r'바이', '구리구리바이구리', result)
    result = re.sub(r'빠이', '구리구리빠이구리', result)    


    result = re.sub(r'사람들', '너굴들', result)

    result = re.sub(r'사람이', '너구리가', result)  # "사람" → "햄스터"
    result = re.sub(r'사람을', '너구리를', result)  # "사람은" → "햄스터는"
    result = re.sub(r'사람이야', '너구리얍', result)  # "사람이야" → "햄스터얌"
    result = re.sub(r'(나는|난)\s*(\S+?)야', '나는 너구리얍', result)  # "나는 [한글]야" → "나는 햄스터얌"
    result = re.sub(r'(나는|난)\s*(\S+?)다[가-힣]?', '나는 너구리닷', result)
    result = re.sub(r'햄스터', r'너구리🦝', result)  # "햄스터" → "햄스터🐹"
    result = re.sub(r'([가-힣])야(?=\s|$|[!?.,])', r'\1얍', result) # "야" → "얌"

    result = re.sub(r'졸리다', '졸리구리..', result)
    result = re.sub(r'잠온다', '잠오는구리..', result)

    # 배고픔 표현
 
    result = re.sub(r'배고파요?', '배고프구리...', result)
    result = re.sub(r'배고프다', '배고프구리...', result)
    

    # 슬픔 표현  
    result = re.sub(r'슬퍼', '슬프구리...', result)
    result = re.sub(r'슬프다', '슬프구리...', result)

    # 심심함 표현
    result = re.sub(r'심심해', '심심하구리...', result)
    result = re.sub(r'심심하다', '심심하구리...', result)

    result = re.sub(r'냐(멍|개|옹|왈)', '냐구리', result)
    result = re.sub(r'다(옹|멍|개|왈|냥)', '다굴', result)
    result = re.sub(r'다\b', '다굴', result)
    result = re.sub(r'요\b', '요구리', result)

    # 5. 대답 변환: "응" → "웅", "네" → "넹", "예" → "녱" (제한적)
    result = re.sub(r'^응(?=[!?\s.,]|$)', '웅', result)
    result = re.sub(r'(\s)응(?=[!?\s.,]|$)', r'\1웅', result)
    # "네"는 명확한 대답일 때만 변환 (문장부호와 함께)
    result = re.sub(r'^네([!?.,])', r'넹\1', result)  # 원본 문장부호 유지
    result = re.sub(r'^네(?=\s*$)', '넹', result)  # 단독으로 끝나는 경우
    result = re.sub(r'(\s)네([!?.,])', r'\1넹\2', result)  # 원본 문장부호 유지
    result = re.sub(r'(\s)네(?=\s*$)', r'\1넹', result)  # 중간에 단독으로 끝나는 경우
    # "예"는 명확한 대답일 때만 변환 (문장부호와 함께)
    result = re.sub(r'^예([!?.,])', r'녱\1', result)  # 원본 문장부호 유지
    result = re.sub(r'^예(?=\s*$)', '녱', result)  # 단독으로 끝나는 경우
    result = re.sub(r'(\s)예([!?.,])', r'\1녱\2', result)  # 원본 문장부호 유지
    result = re.sub(r'(\s)예(?=\s*$)', r'\1녱', result)  # 중간에 단독으로 끝나는 경우
    

    # 6. 감탄사 변환: 문장 맨 앞의 감탄사 변환 (문장 끝 처리 전에 실행)
    result = re.sub(r'^와(?=\s|$|[.!?,:;~])', '후앙', result)
    result = re.sub(r'^오(?=\s|$|[.!?,:;~])', '호오', result)
    result = re.sub(r'^아(?=\s|$|[.!?,:;~])', '후아', result)

        # 7. 감탄사 변환 (앗, 앙, 으악, 아악) - 위치에 관계없이 모두 변환
    result = re.sub(r'(?<![가-힣])앙(?![가-힣])', '후앙', result)  # 앞뒤에 한글이 없는 경우
    result = re.sub(r'(?<![가-힣])앗(?![가-힣])', '후앗', result)  # 앞뒤에 한글이 없는 경우
    result = re.sub(r'(?<![가-힣])으악(?![가-힣])', '후악', result)  # 앞뒤에 한글이 없는 경우
    result = re.sub(r'(?<![가-힣])아악(?![가-힣])', '흐악', result)  # 앞뒤에 한글이 없는 경우

        # 8. 자음 조합 변환 (긴 패턴부터 먼저 처리)
    result = re.sub(r'(ㅎㅇㅌ|화이팅|파이팅)', '너굴팅', result)  # ㅎㅇ보다 먼저 처리
    result = re.sub(r'ㅎㅇ', '구리구리하이구리!', result)
    result = re.sub(r'ㅇㅁ', '어머너굴', result)
    result = re.sub(r'ㅁㅇ', '모야너굴', result)
    result = re.sub(r'(ㄱㅊ|괜찮)', '괜찮너굴', result)
        # ㄱㅇㅇ를 임시로 보호
    result = re.sub(r'ㄱㅇㅇ', 'TEMP_GYY', result)
    # ㅇㅇ 변환
    result = re.sub(r'ㅇㅇ', '웅구리', result)
    result = re.sub(r'(ㅇㄸ|어때|어떰|어뗘)', '구리구리 어떻구리', result)
    result = re.sub(r'(?<![가-힣])아하(?![가-힣])', '구리구리 아하구리', result)  # 앞뒤에 한글이 없는 독립된 "아하"만

    # 10. 문장 끝에 "너굴" 추가 (한국어가 포함된 경우만)
    if re.search(r'[가-힣]', result):
        # 문장 끝 처리 - 문장부호로 끝나는 경우
        result = re.sub(r'([가-힣])(?<!너굴)(\s*[.!?~\\,;]+)(?![가-힣])', r'\1너굴\2', result)

        
        # 이모티콘으로 끝나는 경우
        result = re.sub(r'([가-힣])(?<!너굴)(\s*\^\^\s*$)', r'\1너굴\2', result)  # ^^ 이모티콘
        result = re.sub(r'([가-힣])(?<!너굴)(\s*:\)\s*$)', r'\1너굴\2', result)  # :) 이모티콘
        result = re.sub(r'([가-힣])(?<!너굴)(\s*[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF]+\s*$)', r'\1너굴\2', result)  # 유니코드 이모티콘
        
        # 자음/모음(ㅋㅋ, ㅎㅎ, ㅇㅋ 등) 앞의 한글에 "찍" 추가
        result = re.sub(r'([가-힣])(?<!찍)(\s*[ㄱ-ㅎㅏ-ㅣㅋㅎㅇㅋ]+)', r'\1너굴\2', result)  # 자음/모음 앞
        
        # 줄바꿈 처리
        result = re.sub(r'([가-힣])(?<!찍)(\s*\r?\n)', r'\1너굴\2', result)  # 줄바꿈으로 끝
        
        # 문장부호 없이 끝나는 경우
        result = re.sub(r'([가-힣])(?<!찍)(\s*$)', r'\1너굴\2', result)  # 그냥 끝나는 경우
    
    
    # 12. 불필요한 "찍" 제거 (특별 변환 후 붙은 찍 정리)
    # 단일 패턴 뒤의 찍 제거
    result = re.sub(r'(후앙|호오|구리|굴)너굴', r'\1', result)
    

    result = re.sub(r'TEMP_AA', '아아', result)

    return result
    