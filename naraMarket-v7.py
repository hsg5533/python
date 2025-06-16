import sys
import csv
import json
import logging
import urllib.error
import urllib.request
import concurrent.futures
from urllib.parse import urlencode
from datetime import datetime, timedelta
from PyQt5.QtCore import QThread, pyqtSignal, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QProgressBar, QLineEdit, QLabel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_get_request(url: str, params: dict) -> str:
    """
    지정된 URL에 GET 요청을 보내고 응답 내용을 문자열로 반환하는 함수입니다.
    """
    try:
        query_string = urlencode(params)
        full_url = f"{url}?{query_string}"
        logging.info(f"요청 URL: {full_url}")
        with urllib.request.urlopen(full_url) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        logging.error(f"HTTP Error {e.code}: {e.reason}")
        return f"HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        logging.error(f"URL Error: {e.reason}")
        return f"URL Error: {e.reason}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"

def fetch_all_requests(base_url: str, keywords: list, service_key: str, page_no: str, num_of_rows: str, inqry_bgn_dt: str, inqry_end_dt: str) -> dict:
    """
    여러 키워드에 대해 동시 API 요청을 수행하고 결과를 딕셔너리로 반환합니다.
    """
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
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
                    "bidNtceNm": keyword,
                    "inqryBgnDt": inqry_bgn_dt,
                    "inqryEndDt": inqry_end_dt
                }
            ): keyword for keyword in keywords
        }

        for future in concurrent.futures.as_completed(future_to_keyword):
            keyword = future_to_keyword[future]
            try:
                response = future.result()
                results[keyword] = []
                data = json.loads(response)
                items = data.get('response', {}).get('body', {}).get('items', [])
                if isinstance(items, list):
                    results[keyword].extend(items)
                elif isinstance(items, dict):
                    results[keyword].append(items)
                else:
                    results[keyword].append("알 수 없는 형식의 데이터")
            except Exception as e:
                logging.error(f"Error processing {keyword}: {e}")
                results[keyword] = [f"Error processing {keyword}: {e}"]
    return results

def save_results_to_csv(results: dict, filename: str = "data/results.csv"):
    """
    결과 데이터를 CSV 파일로 저장합니다.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["구분", "입찰공고번호", "키워드", "공고명", "공고기관", "수요기관", "게시일자", "입찰 마감일시"])
        for keyword, bid_list in results.items():
            for bid_item in bid_list:
                if isinstance(bid_item, dict):
                    writer.writerow([
                        bid_item.get("ntceKindNm", ""),
                        f"{bid_item.get('bidNtceNo', '')}-{bid_item.get('bidNtceOrd', '')}",
                        keyword,
                        bid_item.get("bidNtceNm", ""),
                        bid_item.get("ntceInsttNm", ""),
                        bid_item.get("dminsttNm", ""),
                        bid_item.get("bidNtceDt", ""),
                        bid_item.get("bidClseDt", "")
                    ])
        logging.info(f"CSV 저장 완료: {filename}")

class FetchDataThread(QThread):
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, base_url, keywords, service_key, page_no, num_of_rows, inqry_bgn_dt, inqry_end_dt):
        super().__init__()
        self.base_url = base_url
        self.keywords = keywords
        self.service_key = service_key
        self.page_no = page_no
        self.num_of_rows = num_of_rows
        self.inqry_bgn_dt = inqry_bgn_dt
        self.inqry_end_dt = inqry_end_dt

    def run(self):
        try:
            results = fetch_all_requests(self.base_url, self.keywords, self.service_key, self.page_no, self.num_of_rows, self.inqry_bgn_dt, self.inqry_end_dt)
            save_results_to_csv(results)
            self.result_ready.emit(results)
        except Exception as e:
            self.error_occurred.emit(f"오류 발생: {e}")

class ApiFetcherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("API Fetcher")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        self.service_key_input = QLineEdit(self)
        self.layout.addWidget(QLabel("Service Key:"))
        self.layout.addWidget(self.service_key_input)

        self.page_no_input = QLineEdit(self)
        self.layout.addWidget(QLabel("Page Number:"))
        self.layout.addWidget(self.page_no_input)

        self.num_of_rows_input = QLineEdit(self)
        self.layout.addWidget(QLabel("Number of Rows:"))
        self.layout.addWidget(self.num_of_rows_input)

        self.date_input = QLineEdit(self)
        self.date_input.setReadOnly(True)
        self.layout.addWidget(QLabel("선택된 날짜:"))
        self.layout.addWidget(self.date_input)

        self.button_layout = QHBoxLayout()
        for months in [1, 3, 6]:
            btn = QPushButton(f"최근 {months}개월", self)
            btn.clicked.connect(lambda _, m=months: self.set_date_range(m))
            self.button_layout.addWidget(btn)
        self.layout.addLayout(self.button_layout)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        self.fetch_button = QPushButton("데이터 가져오기", self)
        self.fetch_button.clicked.connect(self.on_fetch_button_clicked)
        self.layout.addWidget(self.fetch_button)
        self.setLayout(self.layout)

    def on_fetch_button_clicked(self):
        service_key = self.service_key_input.text().strip()
        page_no = self.page_no_input.text().strip()
        num_of_rows = self.num_of_rows_input.text().strip()
        inqry_bgn_dt, inqry_end_dt = self.date_input.text().split(" ~ ")

        self.fetch_thread = FetchDataThread("https://api.url", [], service_key, page_no, num_of_rows, inqry_bgn_dt, inqry_end_dt)
        self.fetch_thread.result_ready.connect(lambda results: self.text_edit.append(json.dumps(results, indent=4, ensure_ascii=False)))
        self.fetch_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ApiFetcherApp()
    window.show()
    sys.exit(app.exec_())
