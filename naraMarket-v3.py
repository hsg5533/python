from urllib.parse import quote
import urllib.request
import urllib.error
import json
import concurrent.futures
import csv

def serialize(obj: dict) -> str:
    str_list = [f"{quote(str(k))}={quote(str(v))}" for k, v in obj.items()]
    return "&".join(str_list)

def send_get_request(url, param):
    try:
        full_url = url + '?' + serialize(param)
        with urllib.request.urlopen(full_url) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def fetch_all_requests(base_url, keywords):
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_keyword = {executor.submit(send_get_request, base_url, {
            "serviceKey": "Cwy3HRAZ4H8nTNat+MbYSABRgAjVmqkQFOzu2l4pWKTdSgDASF81hpWl7hiklv1YTV6FxPvPp5F2msbGDjXNbg==",
            "pageNo": 1,
            "numOfRows": 10,
            "inqryDiv": 1,
            "type": "json",
            "bidNtceNm": keyword
        }): keyword for keyword in keywords}

        for future in concurrent.futures.as_completed(future_to_keyword):
            keyword = future_to_keyword[future]
            try:
                response = future.result()
                if response:
                    data = json.loads(response)
                    results[keyword] = data.get('response', {}).get('body', {}).get('items', [])
            except Exception as e:
                print(f"Error processing {keyword}: {e}")
    return results

def save_results_to_csv(results, filename="data/results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Keyword", "Item Count"])
        for keyword, count in results.items():
            writer.writerow([keyword, count])

# 예제 사용
data = {"name": "챔버", "age": 25, "city": "서울"}
print(serialize(data))

# 실행 코드
base_url = "https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThngPPSSrch"
keywords = [
    '챔버', 'chamber', 'ssds', '감압챔버', '휴대용 고산소챔버', '이동식 감압실', '고압산소치료기', '표면공기공급', '선별진료소',
    '워크스루 진단부스', '안전도 검사', '기체공급시스템', '호흡기전담클리닉', '심해잠수', '해양경찰청, 중앙해양특수구조단', '해군군수사령부',
    '육군제1266부대', '부산광역시 소방학교', '한국항공우주연구원', '비자성 슈트', '건식 슈트' '습식 슈트' '웻슈트' '드라이 슈트', '스쿠바', '스쿠버', 'scuba', '호흡기',
    '공기충전기', '공기압축기', '수중ROV', '수중드론', '레귤레이터', '실린더', '오리발', '구조장비', '수난장비', '수중통신', '물안경', '수경', '함정장비(다이버리콜시스템)', '다이빙',
    'FACEPIECE', 'REATHING EQUIPMENT', 'DIVING SET', 'DEEP SEA TYPE', 'Closed Circuit Diving Set', 'SEA CONFIDENTAL INFILTRATION'
]

results = fetch_all_requests(base_url, keywords)
print("Final Results:", results)

# 결과를 CSV 파일로 저장
save_results_to_csv(results)
print("Results saved to data/results.csv")
