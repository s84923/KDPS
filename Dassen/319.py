import random

def lottery():
    chance = 205
    total = 65536
    result = random.randint(1, total)

    if result <= chance:
        # 当たりの中で73%の確率で確変
        if random.random() <= 0.73: 
            return "確変！"
        else:
            return "時短！"
    else:
        return "はずれ"

for i in range(1, 101): 
    print(f"{i}回目: {lottery()}")
