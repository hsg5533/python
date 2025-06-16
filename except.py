import random

while True:
     x = random.randint(0,1)  #0~1 사이 랜덤 숫자 추출
     y = random.randint(0,1)  #0~1 사이 랜덤 숫자 추출
     try:
          if y==x+2:
               print('ture')
     except Exception:
          print("error")
     else:
          print("no error")
     finally:
          print("end")
          break
