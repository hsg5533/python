import math   #math 라이브러리 추가

result=list() #결과값 리스트 생성

#피타고라스의 정의를 만족하는 직각삼각형의 길이 찾기
for a in range(1,35):
    for b in range(a+1,45):
        for c in range(b+1,55):
            #빗변의 길이 값이 50이하인 두 변의 길이 구하기
            if (math.sqrt(a**2+b**2)==c and c<=50):
                triangle=(a,b,c)  #직각삼각형의 길이를 튜플로 생성
                result.append(triangle)  #생성된 튜플을 결과값 리스트에 추가

#출력
print("세변의 길이가 50이하의 정수인 직각삼각형의 세변의 쌍 20개입니다.")
for i in result:
    print(i)
                   
