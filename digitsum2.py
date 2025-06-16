total = 0       # total의 값 0으로 설정
answer = "yes"  # answer의 값을 yes로 설정

# answer의 값이 yes이면 반복
while answer == "yes":
    number = int(input("숫자를 입력하시오: "))
    total = total + number
    answer = input("계속?(yes/no): ")

# answer의 값이 no이면 total의 값을 출력
print("합계는 : ", total)
