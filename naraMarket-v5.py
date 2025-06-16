import sys
import csv
import json
import logging
import urllib.error
import urllib.request
import concurrent.futures
from urllib.parse import urlencode
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QProgressBar, QLineEdit, QLabel

# 로깅 설정 (DEBUG 수준으로 설정하면 상세 로그 확인 가능)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_get_request(url: str, params: dict) -> str:
    """
    지정된 URL에 GET 요청을 보내고 응답 내용을 문자열로 반환하는 함수입니다.
    파라미터는 urllib.parse.urlencode를 사용하여 직렬화합니다.
    """
    try:
        # 파라미터를 URL 인코딩
        query_string = urlencode(params)
        full_url = f"{url}?{query_string}"
        logging.info(f"요청 URL: {full_url}")
        with urllib.request.urlopen(full_url) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        error_message = f"HTTP Error {e.code}: {e.reason}"
        logging.error(error_message)
        return error_message
    except urllib.error.URLError as e:
        error_message = f"URL Error: {e.reason}"
        logging.error(error_message)
        return error_message
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        logging.error(error_message)
        return error_message


def fetch_all_requests(base_url: str, keywords: list, service_key: str, page_no: str, num_of_rows: str) -> dict:
    """
    여러 키워드에 대해 동시성 있게 API 요청을 수행하여 결과를 딕셔너리로 반환합니다.
    각 키워드를 key로 하며, API 결과 리스트(또는 오류 메시지)를 value로 저장합니다.
    """
    results = {}
    # 최대 5개의 스레드로 동시 요청
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # 각 키워드에 대해 API 요청 작업을 제출
        future_to_keyword = {
            executor.submit(
                send_get_request, 
                base_url, 
                {
                    "serviceKey": service_key,
                    "pageNo": page_no,
                    "numOfRows": num_of_rows,
                    "inqryDiv": 1,
                    "type": "json",
                    "bidNtceNm": keyword
                }
            ): keyword for keyword in keywords
        }

        # 각 작업의 결과를 처리
        for future in concurrent.futures.as_completed(future_to_keyword):
            keyword = future_to_keyword[future]
            try:
                response = future.result()
                results[keyword] = []  # 초기화
                # JSON 파싱
                data = json.loads(response)
                # JSON 구조에 따른 items 추출
                items = data.get('response', {}).get('body', {}).get('items', [])
                if items:
                    # items가 리스트인 경우
                    if isinstance(items, list):
                        results[keyword].extend(items)
                    # 단일 dict인 경우
                    elif isinstance(items, dict):
                        results[keyword].append(items)
                    else:
                        results[keyword].append("알 수 없는 형식의 데이터")
                else:
                    results[keyword].append("검색된 항목이 없습니다.")
            except Exception as e:
                error_message = f"Error processing {keyword}: {e}"
                logging.error(error_message)
                results[keyword] = [error_message]
    return results


def save_results_to_csv(results: dict, filename: str = "data/results.csv"):
    """
    결과 데이터를 CSV 파일로 저장합니다.
    CSV 파일은 4개의 컬럼(입찰공고번호, 키워드, 공고명, 검색건수)을 갖습니다.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # CSV 헤더 작성
        writer.writerow(["구분","입찰공고번호", "키워드", "공고명", "공고기관", "수요기관", "게시일자", "입찰 마감일시"])
        for keyword, bid_list in results.items():
            for bid_item in bid_list:
                if isinstance(bid_item, dict):
                    # bid_item에서 입찰공고번호와 순번을 조합
                    kind_name = bid_item.get("ntceKindNm", "")
                    bid_no = f"{bid_item.get('bidNtceNo', '')}-{bid_item.get('bidNtceOrd', '')}"
                    bid_name = bid_item.get("bidNtceNm", "")
                    ntce_instt_nm = bid_item.get("ntceInsttNm", "")
                    dm_instt_nm = bid_item.get("dminsttNm", "")
                    bid_ntce_dt = bid_item.get("bidNtceDt", "")
                    bid_clse_dt = bid_item.get("bidClseDt", "")
                    writer.writerow([kind_name,bid_no, keyword, bid_name, ntce_instt_nm, dm_instt_nm, bid_ntce_dt, bid_clse_dt])
        logging.info(f"CSV 파일 저장 완료: {filename}")


class FetchDataThread(QThread):
    """
    API 호출 및 CSV 저장 작업을 별도의 스레드에서 실행하기 위한 QThread 클래스입니다.
    결과가 준비되면 result_ready 시그널을, 오류 발생 시 error_occurred 시그널을 발생시킵니다.
    """
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, base_url: str, keywords: list, service_key: str, page_no: str, num_of_rows: str):
        super().__init__()
        self.base_url = base_url
        self.keywords = keywords
        self.service_key = service_key
        self.page_no = page_no
        self.num_of_rows = num_of_rows

    def run(self):
        try:
            results = fetch_all_requests(self.base_url, self.keywords, self.service_key, self.page_no, self.num_of_rows)
            save_results_to_csv(results)
            # 결과를 메인 스레드에 전달
            self.result_ready.emit(results)
        except Exception as e:
            error_message = f"스레드 실행 중 오류 발생: {e}"
            logging.error(error_message)
            self.error_occurred.emit(error_message)


class ApiFetcherApp(QWidget):
    """
    PyQt5 기반의 API Fetcher GUI 애플리케이션 클래스입니다.
    버튼 클릭 시 백그라운드 스레드에서 API 요청을 실행하고, 결과를 텍스트 에디트에 표시합니다.
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fetch_thread = None  # 백그라운드 스레드 변수

    def initUI(self):
        self.setWindowTitle("API Fetcher")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Service Key 입력란
        self.service_key_label = QLabel("Service Key:", self)
        self.layout.addWidget(self.service_key_label)
        self.service_key_input = QLineEdit(self)
        self.layout.addWidget(self.service_key_input)

        # Page Number 입력란
        self.page_no_label = QLabel("Page Number:", self)
        self.layout.addWidget(self.page_no_label)
        self.page_no_input = QLineEdit(self)
        self.layout.addWidget(self.page_no_input)

        # Number of Rows 입력란
        self.num_of_rows_label = QLabel("Number of Rows:", self)
        self.layout.addWidget(self.num_of_rows_label)
        self.num_of_rows_input = QLineEdit(self)
        self.layout.addWidget(self.num_of_rows_input)

        # 결과 출력용 텍스트 에디트 (읽기 전용)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        # 작업 진행 상황 표시용 프로그레스 바
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)  # 작업 진행 중임을 표시 (무한 진행형)
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        # 데이터 가져오기 버튼
        self.fetch_button = QPushButton("데이터 가져오기", self)
        self.fetch_button.clicked.connect(self.on_fetch_button_clicked)
        self.layout.addWidget(self.fetch_button)

        self.setLayout(self.layout)

    def on_fetch_button_clicked(self):
        """
        버튼 클릭 시 백그라운드 스레드를 시작하여 API 데이터를 가져옵니다.
        작업 진행 동안 버튼은 비활성화되고 프로그레스 바가 표시됩니다.
        """
        # 입력 필드에서 값을 가져옴
        service_key = self.service_key_input.text().strip()
        page_no = self.page_no_input.text().strip()
        num_of_rows = self.num_of_rows_input.text().strip()

        # 필드가 비어있는지 확인
        if not service_key or not page_no or not num_of_rows:
            self.text_edit.append("모든 입력 필드를 채워주세요.")
            return

        self.fetch_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.text_edit.append("데이터를 가져오는 중입니다...")

        base_url = "https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThngPPSSrch"
        keywords = [
            '챔버', 'chamber', 'ssds', '감압 챔버', '휴대용 고산소 챔버', '이동식 감압실', '고압 산소 치료기',
            '표면 공기 공급', '선별 진료소', '워크스루 진단부스', '안전도 검사', '기체 공급 시스템',
            '호흡기 전담 클리닉', '심해 잠수', '해양 경찰청, 중앙 해양 특수 구조단', '해군군수사령부',
            '육군제1266부대', '부산광역시 소방학교', '한국항공우주연구원', '비자성 슈트', '건식 슈트',
            '습식 슈트', '웻슈트', '드라이 슈트', '스쿠바', '스쿠버', 'scuba', '호흡기',
            '공기충전기', '공기압축기', '수중ROV', '수중드론', '레귤레이터', '실린더',
            '오리발', '구조장비', '수난장비', '수중통신', '물안경', '수경',
            '함정장비(다이버리콜시스템)', '다이빙', 'FACEPIECE', 'REATHING EQUIPMENT',
            'DIVING SET', 'DEEP SEA TYPE', 'Closed Circuit Diving Set', 'SEA CONFIDENTAL INFILTRATION'
        ]

        # 백그라운드 스레드 생성 및 시작
        self.fetch_thread = FetchDataThread(base_url, keywords, service_key, page_no, num_of_rows)
        self.fetch_thread.result_ready.connect(self.on_results_ready)
        self.fetch_thread.error_occurred.connect(self.on_error)
        self.fetch_thread.start()

    def on_results_ready(self, results: dict):
        """
        백그라운드 작업이 완료되면 호출되어 결과를 텍스트 에디트에 출력합니다.
        """
        self.text_edit.append("CSV 파일로 결과 저장 완료: data/results.csv")
        self.text_edit.append(json.dumps(results, indent=4, ensure_ascii=False))
        self.fetch_button.setEnabled(True)
        self.progress_bar.setVisible(False)

    def on_error(self, error_message: str):
        """
        백그라운드 작업 중 오류 발생 시 호출되어 오류 메시지를 텍스트 에디트에 출력합니다.
        """
        self.text_edit.append(f"오류 발생: {error_message}")
        self.fetch_button.setEnabled(True)
        self.progress_bar.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ApiFetcherApp()
    window.show()
    sys.exit(app.exec_())
