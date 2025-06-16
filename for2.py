data=[1,2,3,4,5] #data가 저장되는 방식은 0번째 부터 저장된다.
n=len(data) #n은 data의 길이를 의미하므로 5의 값을 가진다.

for i in range(n): #range(n)은 n=5이므로 range(5)와 같아서 범위는 0,1,2,3,4이다. 따라서 i가 가질 수 있는 수는 0,1,2,3,4이다
    x=data[i:] #슬라이싱(slicng) (i:)는 i부터 끝까지를 의미함
    data.append(i+1) #append는 data의 수열 제일 오른쪽에 ()의 수를 추가하는 함수이다.
    print(x) #출력 함수





    
