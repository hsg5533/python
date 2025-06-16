import random

menu = {
    '순한맛': {
        '국물': ['된장찌개', '뭇국', '미역국', '어묵탕', '계란국', '국밥', '북어국'],
        '밥': ['볶음밥', '김밥', '주먹밥', '카레라이스', '유부초밥', '초밥', "(스팸/참치)마요덮밥"],
        '빵/떡': ['햄버거', '토스트', '떡국', '떡만둣국', '피자'],
        '면': ['(순한)라면', '짜장면', '국수', '냉면', '크림파스타', '오일파스타', '토마토 파스타'],
        '튀김': ['치킨', '돈까스', '부추전', '탕수육', '멘보샤', '감자전'],
        '반찬': ['감자전', '김치전', '장조림', '계란말이', '시금치나물']
    },
    '매운맛': {
        '국물': ['김치찌개', '순두부찌개', '마라탕(샹궈)', '부대찌개', '고추장찌개'],
        '밥': ['김치복음밥', '제육덮밥', '짬뽕밥', '비빔밥'],
        '빵/떡': ['피자', '떡꼬치', '떡볶이'],
        '면': ['라면', '짬뽕', '비빔면', '사천짜장', '비빔냉면'],
        '튀김': ['칠리새우', '양념치킨', '김치전', '핫치킨'],
        '반찬': ['오징어젓갈', '어묵볶음', '김치', '무말랭이']
    }
}

def get_menu_option(prompt, options):
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    choice = input("번호를 입력하세요: ")
    return options[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= len(options) else None

food_types = ["국물", "밥", "빵/떡", "면", "튀김", "반찬"]
spicy_levels = ["매운맛", "순한맛"]

food_type = get_menu_option('어떤 음식을 먹고 싶으세요?', food_types)
spicy_level = get_menu_option('어떤 맵기를 원하세요?', spicy_levels)

if food_type and spicy_level:
    category = food_type
    spiciness = spicy_level
    foods = menu[spiciness][category]

    # Remove empty strings from the list of foods
    foods = [food for food in foods if food]

    if foods:
        food = random.choice(foods)
        print(f"\n{food} 추천드립니다!\n")
    else:
        print(f"\n{category} 카테고리에는 음식이 없습니다.\n")
else:
    print("죄송해요... 작동되지 않았어요.")
