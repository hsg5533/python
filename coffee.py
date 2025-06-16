#메뉴 항목을 사전형으로 생성
myCafe={'아메리카노':2500,'아이스아메리카노':3000,'카페라떼':3500,'카푸치노':3500, '카페모카':4000}

#메뉴판 출력
print("========== MENU ==========")
for menu in myCafe:
    print(menu,myCafe[menu])
print("==========================")

#주문 입력받기
noA=int(input("아메리카노 주문량을 입력하세요 (잔): "))
noAA=int(input("아이스 아메리카노 주문량을 입력하세요 (잔): "))
noL=int(input("카페라떼 주문량을 입력하세요 (잔): "))
noC=int(input("카푸치노 주문량을 입력하세요 (잔): "))
noM=int(input("카페모카 주문량을 입력하세요 (잔): "))

#출력
print("주문하신 음료에 대한 결제금액은 %d입니다."%(noA*myCafe['아메리카노']+noAA*myCafe['아이스아메리카노']+noL*myCafe['카페라떼']+noC*myCafe['카푸치노']+noM*myCafe['카페모카']))




