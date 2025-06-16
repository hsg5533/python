for dan in range(2,10):
    for n in range(1,10):
        print(dan,'*',n,'=',dan*n)

# 출력한 단의 숫자 입력
dan = int(input("2-9 사이의 단을 입력하세요: "))

# 2-9 사이의 숫자가 맞게 입력될때 까지 반복
while(dan<2 or dan>9):
    dan = int(input("입력한 값이 잘못되었습니다. 2-9 사이의 정수를 다시  입력하세요: "))

# 2-9 사이의 숫자를 입력받으면 구구단 출력
for n in range(1,10):
    print(dan,'*',n,'=',dan*n)

