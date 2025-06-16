data=[1,2,3,4,5] #data가 저장되는 방식은 0번째 부터 저장된다.
n=len(data)  #n은 data의 길이를 의미하므로 5의 값을 가진다.

for i in range(n): #range(n)은 n=5이므로 범위는 0,1,2,3,4이다. 
    x=data[i:]+data[:i] #슬라이싱(slicng) (i:)는 i부터 끝까지를 의미하고 (:i)는 처음부터 i까지를 의미함.
                        #data[i:]+data[:i]는 두개의 수열을 서로 합치는 것을 의미함
    print(x) #출력함수




   
