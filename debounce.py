import time
import threading  # threading 모듈 추가
from datetime import datetime


def debounce(func=lambda: print(f"Default function executed"), wait=0.25):
    if not callable(func):
        raise TypeError("Expected a function")

    if not isinstance(wait, (int, float)) or wait < 0:
        raise TypeError("Expected wait to be a non-negative number")

    last_args = None
    last_call_time = None
    timer = None
    result = None

    def timer_expired():
        nonlocal timer, last_args, result
        if last_args is not None:
            result = func(*last_args)
            last_args = None
        timer = None

    def debounced_function(*args):
        nonlocal timer, last_args, last_call_time
        current_time = time.time()
        last_args = args
        last_call_time = current_time

        # 타이머를 새로 설정
        if timer is not None:
            timer.cancel()

        # 새로운 타이머를 설정
        timer = threading.Timer(wait, timer_expired)
        timer.start()

        return result

    return debounced_function


# 테스트 함수
def callback():
    print(f"Function executed at {datetime.now().isoformat()}")


# 디바운스된 함수 생성
debounced = debounce()

# 1ms 간격으로 함수 호출
start_time = time.time()


def repeated_calls():
    while time.time() - start_time < 3:
        print("called debounce function")
        debounced()
        time.sleep(0.001)


# 반복 호출 실행
repeated_calls()

print("3 seconds elapsed, forcing final execution...")
