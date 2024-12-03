import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import wikipediaapi
import re

load_dotenv()

# Gemini APIキーの確認
def check_api_key():
    api_key = os.getenv("API_KEY")
    if api_key:
        print(f"API_KEY is set: {api_key[:4]}***")
    else:
        print("Error: API_KEY is not set.")
        return None
    return api_key

# Wikipediaから情報を取得
def get_wikipedia_summary(question_text):
    try:
        wiki = wikipediaapi.Wikipedia(
            language='ja', 
            user_agent="MyApp/1.0 (https://example.com/; you.sou1108@gmail.com)"
        )
        page = wiki.page(question_text)
        if page.exists():
            return page.summary[:500]
        return "関連するWikipediaの情報が見つかりませんでした。"
    except Exception as e:
        print(f"Wikipedia情報の取得中にエラーが発生しました: {e}")
        return "Wikipedia情報の取得に失敗しました。"

# 部分点の計算
def calculate_partial_score(answer, partial_conditions):
    """
    回答に部分点条件がいくつ一致するかを評価し、得点を加算する。
    部分点条件は辞書型 {'キーワード': 点数} または文字列型 'キーワード1:点数, キーワード2:点数' に対応。
    """
    partial_score = 0

    if isinstance(partial_conditions, dict):
        # 辞書型の場合
        try:
            for keyword, score in partial_conditions.items():
                if keyword.strip() in answer:
                    partial_score += int(score)
                    print(f"キーワード '{keyword.strip()}' が一致。部分点: {score}")
        except Exception as e:
            print(f"部分点条件の計算中にエラーが発生しました（辞書型）: {e}")
    elif isinstance(partial_conditions, str):
        # 文字列型の場合
        try:
            conditions = partial_conditions.split(',')
            for condition in conditions:
                if ':' in condition:
                    keyword, score = condition.split(':', 1)
                    if keyword.strip() in answer:
                        partial_score += int(score.strip())
                        print(f"キーワード '{keyword.strip()}' が一致。部分点: {score.strip()}")
                else:
                    print(f"無効な部分点条件の形式: {condition}")
        except Exception as e:
            print(f"部分点条件の計算中にエラーが発生しました（文字列型）: {e}")

    return partial_score

# プロンプト生成
def generate_prompt(question_type, question_text, correct_answer, answer, wikipedia_info, score_max):
    if question_type == "objective":
        return (
            f"模範解答と解答が完全に一致しているかを確認してください。一致していれば「正解」、そうでなければ「不正解」と判断してください。\n"
            f"質問: {question_text}\n"
            f"模範解答: {correct_answer}\n"
            f"解答: {answer}\n"
            f"参考情報: {wikipedia_info}\n"
        )
    else:
        return (
            f"以下の質問に対する模範解答と解答を比較し、内容の一致度を評価し、{score_max}点満点で採点してください。\n"
            f"質問: {question_text}\n"
            f"模範解答: {correct_answer}\n"
            f"解答: {answer}\n"
            f"フィードバックとスコアを提供してください。\n"
        )

# 採点ロジック
def grade_question(question_text, correct_answer, answer, score_max=10, partial_conditions=None):
    api_key = check_api_key()
    if not api_key:
        return "GeminiAPIのAPIキーが設定されていません。", 0

    wikipedia_info = get_wikipedia_summary(question_text)
    question_type = "descriptive" if len(correct_answer.split()) > 1 else "objective"
    prompt = generate_prompt(question_type, question_text, correct_answer, answer, wikipedia_info, score_max)

    # デバッグ情報
    print("デバッグ情報:")
    print(f"質問: {question_text}")
    print(f"模範解答: {correct_answer}")
    print(f"解答: {answer}")
    print(f"部分点条件: {partial_conditions}")
    print(f"スコア上限: {score_max}")

    score = 0  # 初期スコア
    feedback = ""

    try:
        # Gemini APIの呼び出し
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        feedback = response.text.strip()
        print("Gemini APIからのレスポンス:")
        print(feedback)

        # スコアをGemini APIの応答から抽出
        match = re.search(r"(\d+)[/点満点中\s]*(\d+)", feedback)
        if match:
            score = int(match.group(1))
        elif question_type == "objective" and answer.strip() == correct_answer.strip():
            # 選択問題で正解の場合は満点
            score = score_max
        else:
            print("Gemini API応答にスコアが見つかりません。デフォルトで0点とします。")

        # 部分点を加算
        if partial_conditions:
            partial_score = calculate_partial_score(answer, partial_conditions)
            print(f"部分点: {partial_score}")
            score = min(score + partial_score, score_max)

    except Exception as e:
        print(f"APIリクエストエラー: {e}")
        feedback = "フィードバックを生成できませんでした。"
        if partial_conditions:
            partial_score = calculate_partial_score(answer, partial_conditions)
            print(f"部分点（エラー時の計算）: {partial_score}")
            score = partial_score

    # 結果を返す
    return feedback, score
