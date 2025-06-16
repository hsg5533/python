import math

def is_negative(number):
    return number < 0

def main():
    a = input('첫 번째 변의 길이를 입력하세요 > ')
    b = input('두 번째 변의 길이를 입력하세요 > ')

    try:
        a = float(a)
        b = float(b)
    except ValueError:
        print("잘못된 입력입니다. 유효한 숫자를 입력하세요.")
        return

    if a <= 0 or b <= 0:
        print("변의 길이는 양수여야 합니다.")
        return

    c = math.sqrt(a**2 + b**2)

    if not is_negative(c):
        print(f'빗변의 길이: {c:.2f}')
    else:
        print("잘못된 변의 길이입니다. 유효한 직각삼각형을 형성하지 않습니다.")

if __name__ == "__main__":
    main()
