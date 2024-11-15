import random
import time

# 各当選確率
BIG_PROBABILITY = 1/219.9
REG_PROBABILITY = 1/262.1
BUDO_PROBABILITY = 1 / 5.78
CHERRY_PROBABILITY = 1 / 32.29
REPLAY_PROBABILITY = 1 / 7.3

# メダル増減の設定
BIG_REWARD = 300
REG_REWARD = 110
BUDO_REWARD = 8
CHERRY_REWARD = 2
SPIN_COST = 3
MEDALS_PER_INVESTMENT = 46
INVESTMENT_AMOUNT = 1000

class SlotGame:
    def __init__(self):
        self.medals = 46  # 初期メダル数
        self.investment = 1000  # 初期投資額
        self.free_spin = False  # リプレイによる無料スピン
        self.pending_reward = 0  # 次の回転で追加されるメダル枚数
        self.peka_message = None  # ペカッ！の表示メッセージ

    def spin(self):
        # 「ペカッ！！」の表示が必要であれば表示
        if self.peka_message:
            print("ペカッ！！")
            time.sleep(0.5)
            print(self.peka_message)
            self.medals += self.pending_reward
            self.pending_reward = 0
            self.peka_message = None

        if not self.free_spin:
            # 通常スピンでメダルを消費
            self.medals -= SPIN_COST
        self.free_spin = False

        # メダル不足時に追加投資
        if self.medals < 0:
            self.add_investment()

        # 各リールの結果を判定
        if random.random() < BIG_PROBABILITY:
            self.peka_message = "BIG当たり！"
            self.pending_reward = BIG_REWARD
        elif random.random() < REG_PROBABILITY:
            self.peka_message = "REG当たり！"
            self.pending_reward = REG_REWARD
        elif random.random() < BUDO_PROBABILITY:
            result = "ぶどう！ +8枚"
            self.medals += BUDO_REWARD
        elif random.random() < CHERRY_PROBABILITY:
            result = "チェリー！ +2枚"
            self.medals += CHERRY_REWARD
        elif random.random() < REPLAY_PROBABILITY:
            result = "リプレイ！ 次の回転は無料です"
            self.free_spin = True
        else:
            result = "ハズレ..."

        return result if not self.peka_message else "", self.medals, self.investment

    def add_investment(self):
        print("メダルが不足しています。1000円を追加投資し、46枚のメダルを追加します。")
        self.investment += INVESTMENT_AMOUNT
        self.medals += MEDALS_PER_INVESTMENT

# メインループ
def main():
    game = SlotGame()
    print("ジャグラーへようこそ！")
    print(f"現在の持ちメダル: {game.medals}枚, 投資額: {game.investment}円")

    while True:
        input("Enterキーを押してスピン！")  # プレイヤーがスピンを開始
        result, medals, investment = game.spin()
        print("スロットを回しています...")
        time.sleep(1)
        if result:
            print(result)
        print(f"現在の持ちメダル: {medals}枚, 投資額: {investment}円")

# ゲームを開始
if __name__ == "__main__":
    main()
