from urllib.parse import quote
import urllib.request
import urllib.error
import json
import concurrent.futures
import csv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit

def serialize(obj: dict) -> str:
    str_list = [f"{quote(str(k))}={quote(str(v))}" for k, v in obj.items()]
    return "&".join(str_list)

def send_get_request(url, param):
    try:
        full_url = url + '?' + serialize(param)
        with urllib.request.urlopen(full_url) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return f"HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return f"URL Error: {e.reason}"
    except Exception as e:
        return f"Unexpected error: {e}"

def fetch_all_requests(base_url, keywords):
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
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
                    if keyword not in results:
                        results[keyword] = []
                    
                    if len(data['response']['body']['items']) > 0:
                        for item in data['response']['body']['items']:
                            # `bidNtceNm` 값을 하나씩 results에 추가
                            results[keyword].append(item)
                    else:
                        results[keyword].append("검색된 항목이 없습니다.")
            except Exception as e:
                results[keyword] = f"Error processing {keyword}: {e}"

    return results


def save_results_to_csv(results, filename="data/results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["입찰공고번호","키워드", "공고명", "검색건수"])

        for keyword, bid_list in results.items():
            for bid_item in bid_list:
                # Check if bid_item is a dictionary before accessing keys
                if isinstance(bid_item, dict):
                    writer.writerow([bid_item["bidNtceNo"] + '-' + bid_item["bidNtceOrd"],keyword, bid_item["bidNtceNm"], len(bid_list)])
                else:
                    # If it's not a dictionary, write the item as it is
                    writer.writerow([keyword, bid_item, len(bid_list)])


class ApiFetcherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("API Fetcher")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.fetch_button = QPushButton("Fetch Data", self)
        self.fetch_button.clicked.connect(self.fetch_data)
        self.layout.addWidget(self.fetch_button)

        self.setLayout(self.layout)

    def fetch_data(self):
        base_url = "https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThngPPSSrch"
        keywords = [
            '챔버', 'chamber', 'ssds', '감압 챔버', '휴대용 고산소 챔버', '이동식 감압실', '고압 산소 치료기', '표면 공기 공급', '선별 진료소',
            '워크스루 진단부스', '안전도 검사', '기체 공급 시스템', '호흡기 전담 클리닉', '심해 잠수', '해양 경찰청, 중앙 해양 특수 구조단', '해군군수사령부',
            '육군제1266부대', '부산광역시 소방학교', '한국항공우주연구원', '비자성 슈트', '건식 슈트' '습식 슈트' '웻슈트' '드라이 슈트', '스쿠바', '스쿠버', 'scuba', '호흡기',
            '공기충전기', '공기압축기', '수중ROV', '수중드론', '레귤레이터', '실린더', '오리발', '구조장비', '수난장비', '수중통신', '물안경', '수경', '함정장비(다이버리콜시스템)', '다이빙',
            'FACEPIECE', 'REATHING EQUIPMENT', 'DIVING SET', 'DEEP SEA TYPE', 'Closed Circuit Diving Set', 'SEA CONFIDENTAL INFILTRATION'
        ]
        results = fetch_all_requests(base_url, keywords)
        save_results_to_csv(results)
        self.text_edit.append("Results saved to data/results.csv")
        self.text_edit.append(json.dumps(results, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ApiFetcherApp()
    ex.show()
    sys.exit(app.exec_())


# 챔버: 고압 산소 챔버, 산소 챔버, 고압 산소 치료 기챔버, 산소 치료기 챔버, 양압 산소 챔버,음압 산소 챔버, 양음압 산소 챔버, 산소 치료 챔버
# ssds: 해경의 잠수 시스템,