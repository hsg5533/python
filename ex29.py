import numpy as np #numpy라이브러리 불러오고 명령어 np로 변경

ii32 = np.iinfo(np.int32) #np.iinfo(np.int32)를 ii32로 지정
print(type(ii32)) #ii32의 type출력
print(ii32) #ii32의 최솟값과 최댓값 출력
print('\n')

fi64 = np.finfo(np.float64) #np.finfo(np.float64)를 fi64로 지정
print(type(fi64)) #fi64의 type출력
print(fi64) #fi64의 정보 출력