list1 = [1, 2, 3, 4, 5]
list2 = [6, 7, 8, 9]
list3 = list1 + list2
list3.append(0)
print('list3:',list3) #문제1 복붙

if '김희용' in list3: #if문을 사용하여 '김희용'이 있으면 아랫문장 출력
    print("True, list3에 '김희용'이 있음")
else: print("False, list3에 '김희용'이 없음") #그외에 나머지 경우 이 문장 출력

list3.append('김희용') #리스트3에 '김희용'추가
print('list3:',list3) #리스트3 출력

if '김희용' in list3: #위에 복붙
    print("True, list3에 '김희용'이 있음")
else: print("False, list3에 '김희용'이 없음")

list3.reverse #리스트값 반대로 뒤집기
print('list3:',list3)# 리스트3 출력
list3.clear() #리스트 비우기
print('list3:',list3) #리스트3 출력