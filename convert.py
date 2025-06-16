# main.py

# ConvertUnit.py파일을 모듈로 포함
import convertUnit as Unit

# 메뉴 출력
print("-------------------------")
print("   1. 평→제곱미터")
print("   2. 제곱미터→평")
print("   3. 센티미터→인치")
print("   4. 인치→센티미터")
print("   5. 화씨온도→섭씨온도")
print("   6. 섭씨온도→화씨온도")
print("   7. 종료")
print("-------------------------")

# 메뉴 입력받기
while True:
    menu, value=map(float, input("원하는 메뉴와 값을 입력하시오. (예) 1 34   :").split())

    # 결과값 출력
    if menu==1:
        print("%d평 ---> %.2f제곱미터"%(value,Unit.Pyung2msq(value)))
        continue
    if menu==2:
        print("%.2f제곱미터 ---> %d평"%(value,Unit.Msq2pyung(value)))
        continue
    if menu==3:
        print("%d센티미터 ---> %.2f인치"%(value,Unit.Cm2inch(value)))
        continue
    if menu==4:
        print("%.2f인치 ---> %d센티미터"%(value,Unit.Inch2cm(value)))
        continue
    if menu==5:
        print("%.2f화씨온도 ---> %.2f섭씨온도"%(value,Unit.TempF2C(value)))
        continue
    if menu==6:
        print("%.2f섭씨온도 ---> %.2f화씨온도"%(value,Unit.TempC2F(value)))
        continue

    # 종료하기
    if menu==7:
        break
    
