import json
import urllib.error
import urllib.request
from urllib.parse import quote

def serialize(obj: dict) -> str:
    str_list = [f"{quote(str(k))}={quote(str(v))}" for k, v in obj.items()]
    return "&".join(str_list)

def send_get_request(url, param):
    try:
        print(url, param)
        full_url = url + '?' + serialize(param)
        print(full_url)
        with urllib.request.urlopen(full_url) as response:
            print("Headers Information:")
            for header, value in response.headers.items():
                print(f"{header}: {value}")
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# 예제 사용
data = {"name": "챔버", "age": 25, "city": "서울"}
print(serialize(data))


keywords = [
    '챔버', 'chamber', 'ssds', '감압챔버', '휴대용 고산소챔버', '이동식 감압실', '고압산소치료기', '표면공기공급', '선별진료소',
    '워크스루 진단부스', '안전도 검사', '기체공급시스템', '호흡기전담클리닉', '심해잠수', '해양경찰청, 중앙해양특수구조단', '해군군수사령부',
    '육군제1266부대', '부산광역시 소방학교', '한국항공우주연구원', '비자성 슈트', '건식 슈트' '습식 슈트' '웻슈트' '드라이 슈트', '스쿠바', '스쿠버', 'scuba', '호흡기',
    '공기충전기', '공기압축기', '수중ROV', '수중드론', '레귤레이터', '실린더', '오리발', '구조장비', '수난장비', '수중통신', '물안경', '수경', '함정장비(다이버리콜시스템)', '다이빙',
    'FACEPIECE', 'REATHING EQUIPMENT', 'DIVING SET', 'DEEP SEA TYPE', 'Closed Circuit Diving Set', 'SEA CONFIDENTAL INFILTRATION'
]


# API URL 및 파라미터 설정
base_url = "https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThngPPSSrch"


for keyword in keywords:
    print(keyword)
    params = {
        "serviceKey": "Cwy3HRAZ4H8nTNat+MbYSABRgAjVmqkQFOzu2l4pWKTdSgDASF81hpWl7hiklv1YTV6FxPvPp5F2msbGDjXNbg==",
        "pageNo": 1,
        "numOfRows": 10,
        "inqryDiv": 1,
        "type": "json",
        "bidNtceNm": keyword  # 한글 인코딩
    }

    # GET 요청 보내기
    response = send_get_request(base_url, params)
    data = json.loads(response)
    # 응답 결과 출력
    print(len(data['response']['body']['items']))


