#score 이름의 빈 리스트 생성
score=list()

#항상 반복
while True:
    ans=input("점수를 입력하세요.(입력할 점수가 없다면 N을 입력하세요): ")
    #n을 입력받으면 리스트 score의 인덱스 값을 정수형으로 변환하고 반복 중지
    if ans=="n":
        score=list(map(int,score))  
        break
    #0과 100사이의 점수를 입력받으면 리스트에 추가
    elif int(ans)>0 or int(ans)<100:  
        score.append(ans)
    #그 외 값을 입력받으면 다시 입력받음
    else:   
        ans=input("잘못 입력되었습니다. 다시 입력하세요: ")

#출력
print("\n")
print("점수 리스트 : ",score)
print("최고 점수 : ",max(score))
print("최저 점수 : ",min(score))
print("평  .  균 : ",sum(score)/len(score))
