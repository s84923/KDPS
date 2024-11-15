import random
import time

# BIGとREGの当選確率
BIG_PROBABILITY = 1 / 319
REG_PROBABILITY = 1 / 419

def spin_slot():
    # BIG, REG, ハズレの判定
    if random.random() < BIG_PROBABILITY:
        return "BIG当たり！"
    elif random.random() < REG_PROBABILITY:
        return "REG当たり！"
    else:
        return "ハズレ..."

def main():
    print("ジャグラーへようこそ！")
    while True:
        input("Enterキーを押してスピン！")
        result = spin_slot()
        print("スロットを回しています...")
        time.sleep(1)
        print(result)
        
        if result != "ハズレ...":
            break

if __name__ == "__main__":
    main()
