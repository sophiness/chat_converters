import re
import csv
import json

import rule_based_converter.converter.converter_schemas as schemas
from rule_based_converter.converter.dog import dog_converter
from rule_based_converter.converter.cat import cat_converter
from rule_based_converter.converter.hamster import hamster_converter
from rule_based_converter.converter.raccoon import raccoon_converter



def process_csv_simple(input_file, converter, output_file='dog_converted.tsv'):
    """CSV 파일을 읽어서 멍체로 변환 (pandas 없이)"""
    try:
        print(f"📂 파일 읽는 중: {input_file}")
        
        # CSV 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL)
            rows = list(csv_reader)
        
        if not rows:
            print("❌ 파일이 비어있습니다.")
            return
        
        header = rows[0]
        data_rows = rows[1:]
        
        print(f"📊 데이터 개수: {len(data_rows)}줄")
        print(f"📋 헤더: {header}")
        
        # 변환 결과 저장
        results = []
        results.append(['input', 'output'])  # 새 헤더
        
        total_rows = len(data_rows)
        for idx, row in enumerate(data_rows):
            if row and len(row) > 0:
                original_text = row[0]  # 첫 번째 컬럼
                
                converted_text = converter(original_text)
            
                
                results.append([original_text, converted_text])
            
        
        # 결과 저장 (수동으로 TSV 작성하여 따옴표 자동 감싸기 방지)
        with open(output_file.replace('.csv', '.tsv'), 'w', encoding='utf-8-sig') as f:
            # 헤더 작성
            f.write("input\toutput\n")
            
            # 데이터 작성
            for result in results[1:]:  # 헤더 제외
                input_text = result[0]
                output_text = result[1]
                # 탭으로 구분하고 줄바꿈 추가
                f.write(f"{input_text}\t{output_text}\n")
        
        print(f"✅ 변환 완료!")
        print(f"📄 저장된 파일: {output_file.replace('.csv', '.tsv')}")
        print(f"📊 총 {len(results)-1}줄 변환됨")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def process_jsonl_simple(input_file,converter, output_file=None, text_field='content'):
    """JSONL 파일을 읽어서 멍체로 변환하여 input/output 형태로 저장 (pandas 없이)"""
    try:
        if output_file is None:
            output_file = input_file.replace('.jsonl', f'_{converter}.jsonl')
        
        print(f"📂 JSONL 파일 읽는 중: {input_file}")
        
        # JSONL 파일 읽기
        data_rows = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        data_rows.append(data)
                    except json.JSONDecodeError as e:
                        print(f"⚠️  {line_num}번째 줄 JSON 파싱 오류: {e}")
                        continue
        
        if not data_rows:
            print("❌ 파일이 비어있거나 유효한 JSON이 없습니다.")
            return
        
        print(f"📊 데이터 개수: {len(data_rows)}줄")
        print(f"📋 텍스트 필드: '{text_field}'")
        
        # 변환 결과 저장
        total_rows = len(data_rows)
        converted_count = 0
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, data in enumerate(data_rows):
                if text_field in data and data[text_field]:
                    original_text = data[text_field]
                    converted_text = converter(original_text)
                    
                    # input/output 형태로 새로운 데이터 생성
                    new_data = {
                        "input": original_text,
                        "output": converted_text
                    }
                    
                    # JSONL 형식으로 저장
                    f.write(json.dumps(new_data, ensure_ascii=False) + '\n')
                    converted_count += 1
                else:
                    print(f"⚠️  {idx+1}번째 줄에 '{text_field}' 필드가 없거나 비어있습니다.")
                
                # 진행상황 출력
                if (idx + 1) % 10000 == 0:
                    print(f"⏳ 진행중... {idx + 1}/{total_rows}줄 ({(idx + 1)/total_rows*100:.1f}%)")
        
        print(f"✅ 변환 완료!")
        print(f"📄 저장된 파일: {output_file}")
        print(f"📊 총 {total_rows}줄 중 {converted_count}줄 변환됨")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def process_txt_simple(input_file,converter, output_file=None):
    """TXT 파일을 한 줄씩 읽어서 멍체로 변환하여 CSV로 저장 (pandas 없이)"""
    try:
        if output_file is None:
            output_file = input_file.replace('.txt', '_dog.csv')
        
        print(f"📂 TXT 파일 읽는 중: {input_file}")
        
        # TXT 파일 읽기
        lines = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()  # 앞뒤 공백 제거
                if line:  # 빈 줄이 아닌 경우만 처리
                    lines.append(line)
        
        if not lines:
            print("❌ 파일이 비어있거나 유효한 텍스트가 없습니다.")
            return
        
        print(f"📊 데이터 개수: {len(lines)}줄")
        
        # 변환 결과 저장
        results = []
        results.append(['input', 'output'])  # CSV 헤더
        
        total_lines = len(lines)
        for idx, line in enumerate(lines):
            original_text = line
            converted_text = converter(original_text)
            results.append([original_text, converted_text])
            
            # 진행상황 출력
            if (idx + 1) % 10000 == 0:
                print(f"⏳ 진행중... {idx + 1}/{total_lines}줄 ({(idx + 1)/total_lines*100:.1f}%)")
        
        # CSV 파일로 저장
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(results)
        
        print(f"✅ 변환 완료!")
        print(f"📄 저장된 파일: {output_file}")
        print(f"📊 총 {len(results)-1}줄 변환됨")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":


#     #process_csv_simple('strip_data.csv',hamster_converter, 'hamster_converted.tsv')
#     #process_txt_simple('sns_corpus.txt','hamster_converter', 'hamster_converted.csv')
    # print(hamster_converter('안뇽여러분😎 나는 호두야'))
    process_jsonl_simple('data.jsonl', raccoon_converter, 'rac_converted.jsonl', text_field='content')