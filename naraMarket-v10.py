import sys
import json
import logging
import urllib.error
import urllib.request
import concurrent.futures
from urllib.parse import urlencode

# Excel 파일 생성을 위한 openpyxl 모듈 import
from openpyxl import Workbook

from PyQt5.QtCore import QThread, pyqtSignal, QDate
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QProgressBar, QLineEdit, QLabel, QMessageBox
)

# 로깅 설정 (INFO 수준)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_get_request(url: str, params: dict, timeout: int = 10) -> str:
    """
    지정된 URL에 GET 요청을 보내고 응답 내용을 문자열로 반환합니다.
    :param url: API 기본 URL
    :param params: GET 파라미터 (dict)
    :param timeout: 요청 타임아웃 (초)
    :return: 응답 문자열 또는 오류 메시지
    """
    try:
        # 파라미터를 URL 인코딩
        query_string = urlencode(params)
        full_url = f"{url}?{query_string}"
        logging.info(f"요청 URL: {full_url}")
        # 타임아웃 설정 추가
        with urllib.request.urlopen(full_url, timeout=timeout) as response:
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


def fetch_all_requests(base_url: str, keywords: list, service_key: str, page_no: str,
                       num_of_rows: str, inqry_bgn_dt: str, inqry_end_dt: str,
                       progress_callback=None) -> dict:
    """
    여러 키워드에 대해 동시성 있게 API 요청을 수행하고 결과를 딕셔너리로 반환합니다.
    각 키워드별로 요청 후 진행률을 progress_callback 함수를 통해 전달할 수 있습니다.
    
    :param base_url: API 기본 URL
    :param keywords: 검색할 키워드 리스트
    :param service_key: 서비스 키
    :param page_no: 페이지 번호
    :param num_of_rows: 한 페이지당 행(row) 수
    :param inqry_bgn_dt: 조회 시작일자 (yyyyMMdd)
    :param inqry_end_dt: 조회 종료일자 (yyyyMMdd)
    :param progress_callback: (optional) 진행률 업데이트를 위한 콜백 함수. (completed, total)
    :return: {키워드: [API 결과, ...], ...}
    """
    results = {}
    total = len(keywords)
    completed = 0

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
                    "inqryEndDt": inqry_end_dt,
                }
            ): keyword for keyword in keywords
        }

        for future in concurrent.futures.as_completed(future_to_keyword):
            keyword = future_to_keyword[future]
            try:
                response = future.result()
                results[keyword] = []
                # JSON 파싱 시 에러 발생할 경우를 대비하여 try/except 처리
                try:
                    data = json.loads(response)
                except json.JSONDecodeError:
                    results[keyword].append("JSON 파싱 오류")
                    continue

                # API 응답 구조에 따라 items 추출
                items = data.get('response', {}).get('body', {}).get('items', [])
                if items:
                    if isinstance(items, list):
                        results[keyword].extend(items)
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
            # 진행률 업데이트: 완료 건수 증가 후 콜백 호출
            completed += 1
            if progress_callback:
                progress_callback(completed, total)
    return results


def save_results_to_excel(results: dict, filename: str = "results.xlsx"):
    """
    결과 데이터를 Excel 파일로 저장합니다.
    Excel 파일은 8개의 컬럼(구분, 입찰공고번호, 키워드, 공고명, 공고기관, 수요기관, 게시일자, 입찰 마감일시)을 갖습니다.
    
    :param results: API 요청 결과 딕셔너리
    :param filename: 저장할 파일명 (기본값: results.xlsx)
    """
    try:
        # 새 Workbook 생성
        wb = Workbook()
        ws = wb.active
        ws.title = "Results"
        # Excel 헤더 작성
        headers = ["구분", "입찰공고번호", "키워드", "공고명", "공고기관", "수요기관", "게시일자", "입찰 마감일시"]
        ws.append(headers)
        # 결과 데이터를 각 행에 작성
        for keyword, bid_list in results.items():
            for bid_item in bid_list:
                if isinstance(bid_item, dict):
                    kind_name = bid_item.get("ntceKindNm", "")
                    bid_no = f"{bid_item.get('bidNtceNo', '')}-{bid_item.get('bidNtceOrd', '')}"
                    bid_name = bid_item.get("bidNtceNm", "")
                    ntce_instt_nm = bid_item.get("ntceInsttNm", "")
                    dm_instt_nm = bid_item.get("dminsttNm", "")
                    bid_ntce_dt = bid_item.get("bidNtceDt", "")
                    bid_clse_dt = bid_item.get("bidClseDt", "")
                    ws.append([kind_name, bid_no, keyword, bid_name, ntce_instt_nm, dm_instt_nm, bid_ntce_dt, bid_clse_dt])
        # Excel 파일 저장
        wb.save(filename)
        logging.info(f"엑셀 파일 저장 완료: {filename}")
    except Exception as e:
        logging.error(f"엑셀 저장 오류: {e}")


class FetchDataThread(QThread):
    """
    API 호출 및 Excel 저장 작업을 별도의 스레드에서 실행하기 위한 QThread 클래스입니다.
    작업 진행률(progress_update)도 메인 UI에 전달합니다.
    """
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(int)  # 진행률(0~100) 업데이트를 위한 시그널

    def __init__(self, base_url: str, keywords: list, service_key: str, page_no: str,
                 num_of_rows: str, inqry_bgn_dt: str, inqry_end_dt: str):
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
            # progress_callback: 각 작업 완료 시 진행률(%)를 계산하여 시그널 발행
            def progress_callback(completed, total):
                percent = int((completed / total) * 100)
                self.progress_update.emit(percent)

            results = fetch_all_requests(
                self.base_url, self.keywords, self.service_key, self.page_no,
                self.num_of_rows, self.inqry_bgn_dt, self.inqry_end_dt,
                progress_callback=progress_callback
            )
            # Excel 파일로 결과 저장
            save_results_to_excel(results)
            self.result_ready.emit(results)
        except Exception as e:
            error_message = f"스레드 실행 중 오류 발생: {e}"
            logging.error(error_message)
            self.error_occurred.emit(error_message)


class ApiFetcherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fetch_thread = None  # 백그라운드 스레드 객체

    def initUI(self):
        self.setWindowTitle("API Fetcher")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        # 서비스 키 입력
        service_key_layout = QHBoxLayout()
        self.service_key_label = QLabel("서비스키:", self)
        service_key_layout.addWidget(self.service_key_label)
        self.service_key_input = QLineEdit(self)
        service_key_layout.addWidget(self.service_key_input)
        self.layout.addLayout(service_key_layout)

        # 페이지 번호 입력
        page_no_layout = QHBoxLayout()
        self.page_no_label = QLabel("조회페이지:", self)
        page_no_layout.addWidget(self.page_no_label)
        self.page_no_input = QLineEdit(self)
        page_no_layout.addWidget(self.page_no_input)
        self.layout.addLayout(page_no_layout)

        # 한 페이지당 행(row) 수 입력
        num_of_rows_layout = QHBoxLayout()
        self.num_of_rows_label = QLabel("조회갯수:", self)
        num_of_rows_layout.addWidget(self.num_of_rows_label)
        self.num_of_rows_input = QLineEdit(self)
        num_of_rows_layout.addWidget(self.num_of_rows_input)
        self.layout.addLayout(num_of_rows_layout)

        # 시작일자 및 종료일자 표시 (버튼으로 설정)
        date_layout = QHBoxLayout()
        self.start_date_input = QLineEdit(self)
        self.start_date_input.setReadOnly(True)
        date_layout.addWidget(QLabel("시작일자:"))
        date_layout.addWidget(self.start_date_input)

        self.end_date_input = QLineEdit(self)
        self.end_date_input.setReadOnly(True)
        date_layout.addWidget(QLabel("종료일자:"))
        date_layout.addWidget(self.end_date_input)
        self.layout.addLayout(date_layout)

        # 최근 1, 3, 6개월 버튼 (날짜 자동 설정)
        self.button_layout = QHBoxLayout()
        for months in [1, 3, 6]:
            btn = QPushButton(f"최근 {months}개월", self)
            # lambda의 기본 인자 m=months로 클로저 문제 해결
            btn.clicked.connect(lambda _, m=months: self.set_date_range(m))
            self.button_layout.addWidget(btn)
        self.layout.addLayout(self.button_layout)

        # 결과 출력용 텍스트 에디트 (읽기 전용)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        # 작업 진행 상황 표시용 프로그레스바 (0~100)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        # 데이터 가져오기 버튼
        self.fetch_button = QPushButton("데이터 가져오기", self)
        self.fetch_button.clicked.connect(self.on_fetch_button_clicked)
        self.layout.addWidget(self.fetch_button)

        self.setLayout(self.layout)

    def on_fetch_button_clicked(self):
        """
        데이터 가져오기 버튼 클릭 시 입력값 검증 후 백그라운드 스레드에서 API 호출을 시작합니다.
        """
        service_key = self.service_key_input.text().strip()
        page_no = self.page_no_input.text().strip()
        num_of_rows = self.num_of_rows_input.text().strip()
        start_date = self.start_date_input.text().strip()
        end_date = self.end_date_input.text().strip()

        # 날짜 및 필수 입력값 검증
        if not start_date or not end_date:
            self.text_edit.append("시작일자와 종료일자를 선택해주세요.")
            return
        if not service_key or not page_no or not num_of_rows:
            self.text_edit.append("모든 입력 필드를 채워주세요.")
            return
        # 페이지 번호와 행 수는 숫자여야 함
        if not page_no.isdigit() or not num_of_rows.isdigit():
            self.text_edit.append("Page Number와 Number of Rows는 숫자여야 합니다.")
            return

        # UI 상태 업데이트
        self.fetch_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.text_edit.append("데이터를 가져오는 중입니다...")

        base_url = "https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThngPPSSrch"
        keywords = [
            '챔버', 'chamber', 'ssds', '감압 챔버', '휴대용 고산소 챔버', '이동식 감압실', '고압 산소 치료기',
            '표면 공기 공급', '선별 진료소', '워크스루 진단부스', '안전도 검사', '기체 공급 시스템',
            '호흡기 전담 클리닉', '심해 잠수', '해양 경찰청, 중앙 해양 특수 구조단', '해군군수사령부',
            '육군제1266부대', '부산광역시 소방학교', '한국항공우주연구원', '비자성 슈트', '건식 슈트',
            '습식 슈트', '웻슈트', '드라이 슈트', '스쿠바', '스쿠버', 'scuba', '호흡기',
            '공기충전기', '공기압축기', '수중ROV', '수중드론', '레귤레이터', '실린더',
            '오리발', '구조장비', '수난장비', '인공호흡기'
        ]

        # 백그라운드 스레드 생성 및 시작
        self.fetch_thread = FetchDataThread(
            base_url,
            keywords,
            service_key,
            page_no,
            num_of_rows,
            start_date,  # 조회 시작일자
            end_date     # 조회 종료일자
        )
        self.fetch_thread.result_ready.connect(self.on_data_fetched)
        self.fetch_thread.error_occurred.connect(self.on_error_occurred)
        self.fetch_thread.progress_update.connect(self.on_progress_update)
        self.fetch_thread.start()

    def on_progress_update(self, value):
        """
        백그라운드 스레드로부터 전달받은 진행률(%)을 프로그레스바에 반영합니다.
        """
        self.progress_bar.setValue(value)

    def on_data_fetched(self, results):
        """
        API 호출 및 Excel 저장 작업 완료 후 결과를 출력합니다.
        """
        self.text_edit.clear()
        self.text_edit.append("엑셀 파일로 결과 저장 완료: results.xlsx")
        # 보기 좋게 JSON 포맷으로 출력
        self.text_edit.append(json.dumps(results, indent=2, ensure_ascii=False))
        self.fetch_button.setEnabled(True)
        self.progress_bar.setVisible(False)

    def on_error_occurred(self, error_message):
        """
        작업 중 오류가 발생하면 오류 메시지를 출력합니다.
        """
        self.text_edit.clear()
        self.text_edit.append(f"오류 발생: {error_message}")
        QMessageBox.critical(self, "오류", error_message)
        self.fetch_button.setEnabled(True)
        self.progress_bar.setVisible(False)

    def set_date_range(self, months):
        """
        최근 X개월 버튼 클릭 시 현재 날짜를 기준으로 시작일자와 종료일자를 설정합니다.
        날짜 형식은 yyyyMMdd입니다.
        """
        today = QDate.currentDate()
        end_date = today.toString("yyyyMMdd")
        start_date = today.addMonths(-months).toString("yyyyMMdd")
        self.start_date_input.setText(start_date)
        self.end_date_input.setText(end_date)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ApiFetcherApp()
    window.show()
    sys.exit(app.exec())
