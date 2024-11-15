import random
import os
from playsound import playsound

# 定数設定
CHANCE_ATARI = 205
CHANCE_TOTAL = 65536
CHANCE_KAKUHEN = 656
COST_PER_1000YEN = 250  # 1000円で借りられる玉数
SPINS_PER_250_BALLS_MIN = 11  # 250玉での最小回転数
SPINS_PER_250_BALLS_MAX = 25  # 250玉での最大回転数

# 玉の増減
NORMAL_REWARD = 300        # 通常当たりの玉数
KAKUHEN_REWARD = 1500      # 確変中の当たりの玉数

# 色設定
RESET_COLOR = "\033[0m"
GREEN_COLOR = "\033[92m"
YELLOW_COLOR = "\033[93m"

# 音声ファイルのパス
sound_file_path = os.path.abspath('Dassen/kyu.wav')  # WAV形式の音声ファイル

def play_sound():
    """音声を再生"""
    print(f"再生する音声ファイルのパス: {sound_file_path}")
    try:
        playsound(sound_file_path)
    except Exception as e:
        print(f"音声再生エラー: {e}")

def lottery():
    result = random.randint(1, CHANCE_TOTAL)
    if result <= CHANCE_ATARI:
        if random.random() <= 0.73:
            play_sound()  # 確変大当たり時の音再生
            print(GREEN_COLOR + "シンインパクトラッシュ！" + RESET_COLOR)
            input("次の回転をするにはEnterキーを押してください...")
            return True  # 確変大当たり
        else:
            print(YELLOW_COLOR + "チャンスタイム！" + RESET_COLOR)
            input("次の回転をするにはEnterキーを押してください...")
            return False  # 通常の当たり
    else:
        print("はずれ")
        return None  # 当たりではない場合

def kakuhen_lottery():
    total_balls = 0   # 確変中に獲得した総玉数
    kakuhen_count = 1  # 確変中の大当たり回数をカウント

    for spin in range(1, 164):
        result = random.randint(1, CHANCE_TOTAL)
        print(f"インパクトラッシュ{spin}回転目:", end=" ")
        
        if result <= CHANCE_KAKUHEN:
            play_sound()  # 確変中の当たり時に音を再生
            print(GREEN_COLOR + f"インパクトラッシュ{kakuhen_count}回目{KAKUHEN_REWARD}玉獲得！" + RESET_COLOR)
            total_balls += KAKUHEN_REWARD
            kakuhen_count += 1  # 確変中の大当たり回数を増加
            
            input("次の回転をするにはEnterキーを押してください...")
        else:
            print("はずれ")
    return total_balls  # 確変終了時の総獲得玉数を返す

def play_game():
    total_investment = 1000  # 初回投資額
    total_balls = 0          # 総獲得玉数
    spin_count = 1           # 試行回数を管理

    while True:
        # 1000円で250玉を借りる -> 15〜21回転のみ試行
        spins = random.randint(SPINS_PER_250_BALLS_MIN, SPINS_PER_250_BALLS_MAX)
        
        # 試行する
        for _ in range(spins):
            print(f"{spin_count}回目: ", end="")
            result = lottery()
            spin_count += 1

            if result is not None:  # 当たりが出た場合
                if result:  # 確変大当たりの初回は300玉のみ獲得
                    total_balls += NORMAL_REWARD
                    print(GREEN_COLOR + f"シンインパクトラッシュ突入！{NORMAL_REWARD}玉獲得！" + RESET_COLOR)
                    total_balls += kakuhen_lottery()  # 確変モードでの総獲得玉数を追加
                    print(f"\nシンインパクトラッシュ終了。総獲得玉数: {total_balls}玉")
                    print(f"総投資額: {total_investment}円")
                    return  # ゲーム終了
                else:  # 通常の当たり
                    print(f"チャンスタイム突入！{NORMAL_REWARD}玉獲得！")
                    total_balls += NORMAL_REWARD

        # 回転数終了後、追加投資の確認
        choice = input(f"追加投資するにはEnterを押してください。総投資額: {total_investment}円")
        if choice == '':  # エンターキーで追加投資
            total_investment += 1000
            print(f"\n現在の総投資額: {total_investment}円")
        else:
            print("\n終了。")
            print(f"総投資額: {total_investment}円")
            print(f"総獲得玉数: {total_balls}玉")
            print(f"最終試行回数: {spin_count - 1}回")
            return  # ゲーム終了

# 実行
play_game()
