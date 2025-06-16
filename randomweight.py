import random

def get_random_weighted_item(items):
    total_weight = sum(prob * item[1] for prob, item in zip(probabilities, items))
    random_weight = random.random() * total_weight
    accumulated_weight = 0

    for prob, item in zip(probabilities, items):
        accumulated_weight += prob * item[1]
        if random_weight <= accumulated_weight:
            return item[0]

# test ------------------------------------------
numbers = [10, 15, 20, 25, 30]
probabilities = [0.5, 20, 0.3, 0.2, 0.1]

items = list(zip(numbers, probabilities))

selected = get_random_weighted_item(items)
print(f"선택된 아이템: {selected}")


def get_random_weighted_item2():
    numbers = [10, 15, 20, 25, 30]
    probabilities = [50, 0.2, 0.3, 0.2, 0.1]

    items = list(zip(numbers, probabilities))

    total_weight = sum(prob * item[1] for prob, item in zip(probabilities, items))
    random_weight = random.random() * total_weight
    accumulated_weight = 0

    for prob, item in zip(probabilities, items):
        accumulated_weight += prob * item[1]
        if random_weight <= accumulated_weight:
            return item[0]

# test ------------------------------------------
selected = get_random_weighted_item2()
print(f"선택된 아이템: {selected}")

def generate_random_number_with_probability():
    # 10부터 30까지의 숫자와 각 숫자에 대한 확률을 정의
    numbers = [10, 15, 20, 25, 30]
    probabilities = [0.3, 0.2, 0.3, 0.2, 0.1]

    return random.choices(numbers, probabilities)[0]


print(generate_random_number_with_probability())