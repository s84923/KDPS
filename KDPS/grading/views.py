from django.shortcuts import render, redirect, get_object_or_404
from KDPS.models import Question, GeminiTest, TempAnswer, ConversationHistory, GradingCriteria
from .forms import QuestionForm
from .scoring import grade_question  # scoring.pyから採点機能をインポート

# ホーム画面 - 試験リストを表示
def home(request):
    tests = GeminiTest.objects.all()
    return render(request, "home.html", {"tests": tests})

# 問題作成画面
def create_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            # 配点の設定
            score = request.POST.get("score", 10)  # デフォルトで10点
            question.score = int(score)

            # 部分点条件の設定
            partial_scoring_conditions = request.POST.get("partial_scoring_conditions", "")
            question.partial_scoring_conditions = partial_scoring_conditions

            question.save()
            return redirect("home")
    else:
        form = QuestionForm()
    return render(request, "create_question.html", {"form": form})

# 試験選択画面
def select_test(request):
    tests = GeminiTest.objects.all()
    return render(request, "select_test.html", {"tests": tests})

# 試験開始画面 - 問題リストを表示
def start_test(request, test_id):
    test = get_object_or_404(GeminiTest, id=test_id)
    questions = test.questions.all()
    return render(request, "start_test.html", {"test": test, "questions": questions})

# 問題解答画面
def answer_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    test = question.test  # 該当する問題に関連する試験情報を取得

    # 現在の問題に対応する一時保存回答を取得
    temp_answer = TempAnswer.objects.filter(question=question, is_finalized=False).first()

    if request.method == "POST":
        answer_text = request.POST.get("answer")  # 解答を取得

        if not answer_text:
            return render(request, "answer_question.html", {
                "question": question,
                "test": test,
                "temp_answer": temp_answer,
                "error_message": "回答が入力されていません。"
            })

        if "save" in request.POST:
            # 一時保存ボタンが押された場合
            if temp_answer:
                temp_answer.answer_text = answer_text
                temp_answer.save()
            else:
                TempAnswer.objects.create(
                    question=question,
                    answer_text=answer_text,
                    is_finalized=False,
                    user_id=1  # 仮のユーザーID
                )
            return render(request, "answer_question.html", {
                "question": question,
                "test": test,
                "temp_answer": temp_answer,
                "success_message": "解答が一時保存されました。"
            })

        if "submit" in request.POST:
            if temp_answer:
                temp_answer.is_finalized = True
                temp_answer.save()

                # 最終提出後に未提出の一時保存解答を削除
                TempAnswer.objects.filter(question=question, is_finalized=False).delete()

                # 過去のフィードバックとスコアを削除
                ConversationHistory.objects.filter(question=question).delete()

                # 部分点条件の取得
                partial_conditions = question.get_partial_conditions()

                # 新しいフィードバックを生成して保存
                feedback, score = grade_question(
                    temp_answer.question.content,
                    temp_answer.question.correct_answer,
                    temp_answer.answer_text,
                    temp_answer.question.score,
                    partial_conditions=partial_conditions
                )

                # 新しいフィードバックを保存
                ConversationHistory.objects.create(
                    question=temp_answer.question,
                    user_answer=temp_answer.answer_text,
                    feedback=feedback,
                    score=score
                )
            return redirect("start_test", test_id=test.id)

    return render(request, "answer_question.html", {
        "question": question,
        "test": test,
        "temp_answer": temp_answer
    })

# 解答の最終提出
def submit_answers(request, test_id):
    if request.method == "POST":
        temp_answers = TempAnswer.objects.filter(question__test_id=test_id, is_finalized=False)
        total_score = 0

        # 古いフィードバックを削除
        ConversationHistory.objects.filter(question__test_id=test_id).delete()

        for temp_answer in temp_answers:
            # 部分点条件の取得
            partial_conditions = temp_answer.question.get_partial_conditions()

            feedback, score = grade_question(
                temp_answer.question.content,
                temp_answer.question.correct_answer,
                temp_answer.answer_text,
                temp_answer.question.score,
                partial_conditions=partial_conditions
            )

            # 最終提出としてマーク
            temp_answer.is_finalized = True
            temp_answer.save()

            # 結果を保存
            ConversationHistory.objects.create(
                question=temp_answer.question,
                user_answer=temp_answer.answer_text,
                feedback=feedback,
                score=score
            )
            total_score += score

        # 一時保存データを削除
        temp_answers.delete()

        test = get_object_or_404(GeminiTest, id=test_id)
        test.total_score = total_score
        test.save()

        return redirect("show_results", test_id=test_id)

# 採点結果表示画面
def show_results(request, test_id):
    test = get_object_or_404(GeminiTest, id=test_id)
    history = ConversationHistory.objects.filter(question__test=test)
    total_score = sum([entry.score for entry in history if entry.score is not None])
    return render(request, "show_results.html", {
        "test": test,
        "history": history,
        "total_score": total_score,
        "max_score": test.total_score
    })

# 採点基準設定画面
def set_grading_criteria(request, test_id):
    test = get_object_or_404(GeminiTest, id=test_id)
    criteria = GradingCriteria.objects.filter(test=test).first()

    if request.method == "POST":
        description = request.POST.get("criteria")
        if criteria:
            criteria.description = description
            criteria.save()
        else:
            GradingCriteria.objects.create(test=test, description=description)
        return redirect("show_results", test_id=test_id)

    return render(request, "set_grading_criteria.html", {"test": test, "current_criteria": criteria})
