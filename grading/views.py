from django.shortcuts import render, redirect, get_object_or_404
from KDPS.models import Question, Test, TempAnswer, ConversationHistory, GradingCriteria
from .forms import QuestionForm
from .scoring import grade_question  # 採点機能をインポート

# ホーム画面 - 試験リストを表示
def home(request):
    """
    ホーム画面。Testモデルのリストを表示。
    """
    tests = Test.objects.all()
    return render(request, "home.html", {"tests": tests})

# 生徒用ホーム画面 - 試験リストを表示
def studenthome(request):
    """
    ホーム画面。Testモデルのリストを表示。
    """
    tests = Test.objects.all()
    return render(request, "studenthome.html", {"tests": tests})

# 試験選択画面
def select_test(request):
    """
    試験を選択するための画面を表示するビュー。
    """
    tests = Test.objects.all()
    return render(request, "select_test.html", {"tests": tests})

# 問題作成画面
def create_question(request):
    """
    新しい問題を作成するビュー。
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.score = int(request.POST.get("score", 10))  # 配点の設定（デフォルト10点）
            question.partial_scoring_conditions = request.POST.get("partial_scoring_conditions", "")
            question.save()
            return redirect("home")
    else:
        form = QuestionForm()
    return render(request, "create_question.html", {"form": form})

# 試験開始画面 - 問題リストを表示
def start_test(request, test_id):
    """
    選択した試験の問題リストを表示するビュー。
    """
    test = get_object_or_404(Test, test_id=test_id)
    questions = test.questions.all()
    return render(request, "start_test.html", {"test": test, "questions": questions})

# 生徒試験開始画面 - 問題リストを表示
def studentstart_test(request, test_id):
    """
    選択した試験の問題リストを表示するビュー。
    """
    test = get_object_or_404(Test, test_id=test_id)
    questions = test.questions.all()
    return render(request, "studentstart_test.html", {"test": test, "questions": questions})

# 問題解答画面
def answer_question(request, question_id):
    """
    各問題に対する解答を入力するビュー。
    """
    question = get_object_or_404(Question, id=question_id)
    test = question.test
    temp_answer = TempAnswer.objects.filter(question=question, is_finalized=False).first()

    if request.method == "POST":
        answer_text = request.POST.get("answer")
        if not answer_text:
            return render(request, "answer_question.html", {
                "question": question,
                "test": test,
                "temp_answer": temp_answer,
                "error_message": "回答が入力されていません。"
            })

        if "save" in request.POST:
            # 一時保存
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
            # 最終提出
            if temp_answer:
                temp_answer.is_finalized = True
                temp_answer.save()
                TempAnswer.objects.filter(question=question, is_finalized=False).delete()
                ConversationHistory.objects.filter(question=question).delete()
                partial_conditions = question.get_partial_conditions()
                feedback, score = grade_question(
                    temp_answer.question.content,
                    temp_answer.question.correct_answer,
                    temp_answer.answer_text,
                    temp_answer.question.score,
                    partial_conditions=partial_conditions
                )
                ConversationHistory.objects.create(
                    question=temp_answer.question,
                    user_answer=temp_answer.answer_text,
                    feedback=feedback,
                    score=score
                )
            return redirect("start_test", test_id=test.test_id)

    return render(request, "answer_question.html", {
        "question": question,
        "test": test,
        "temp_answer": temp_answer
    })

# 生徒問題解答画面
def studentanswer_question(request, question_id):
    """
    各問題に対する解答を入力するビュー。
    """
    question = get_object_or_404(Question, id=question_id)
    test = question.test
    temp_answer = TempAnswer.objects.filter(question=question, is_finalized=False).first()

    if request.method == "POST":
        answer_text = request.POST.get("answer")
        if not answer_text:
            return render(request, "studentanswer_question.html", {
                "question": question,
                "test": test,
                "temp_answer": temp_answer,
                "error_message": "回答が入力されていません。"
            })

        if "save" in request.POST:
            # 一時保存
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
            return render(request, "studentanswer_question.html", {
                "question": question,
                "test": test,
                "temp_answer": temp_answer,
                "success_message": "解答が一時保存されました。"
            })

        if "submit" in request.POST:
            # 最終提出
            if temp_answer:
                temp_answer.is_finalized = True
                temp_answer.save()
                TempAnswer.objects.filter(question=question, is_finalized=False).delete()
                ConversationHistory.objects.filter(question=question).delete()
                partial_conditions = question.get_partial_conditions()
                feedback, score = grade_question(
                    temp_answer.question.content,
                    temp_answer.question.correct_answer,
                    temp_answer.answer_text,
                    temp_answer.question.score,
                    partial_conditions=partial_conditions
                )
                ConversationHistory.objects.create(
                    question=temp_answer.question,
                    user_answer=temp_answer.answer_text,
                    feedback=feedback,
                    score=score
                )
            return redirect("studentstart_test", test_id=test.test_id)

    return render(request, "studentanswer_question.html", {
        "question": question,
        "test": test,
        "temp_answer": temp_answer
    })

# 解答の最終提出
def submit_answers(request, test_id):
    """
    全ての解答を最終提出するビュー。
    """
    if request.method == "POST":
        temp_answers = TempAnswer.objects.filter(question__test_id=test_id, is_finalized=False)
        total_score = 0
        ConversationHistory.objects.filter(question__test_id=test_id).delete()

        for temp_answer in temp_answers:
            partial_conditions = temp_answer.question.get_partial_conditions()
            feedback, score = grade_question(
                temp_answer.question.content,
                temp_answer.question.correct_answer,
                temp_answer.answer_text,
                temp_answer.question.score,
                partial_conditions=partial_conditions
            )
            temp_answer.is_finalized = True
            temp_answer.save()
            ConversationHistory.objects.create(
                question=temp_answer.question,
                user_answer=temp_answer.answer_text,
                feedback=feedback,
                score=score
            )
            total_score += score

        temp_answers.delete()

        test = get_object_or_404(Test, test_id=test_id)
        test.total_score = total_score  # 必要に応じて変更
        test.save()

        return redirect("show_results", test_id=test_id)

def studentsubmit_answers(request, test_id):
    """
    全ての解答を最終提出するビュー。
    """
    if request.method == "POST":
        temp_answers = TempAnswer.objects.filter(question__test_id=test_id, is_finalized=False)
        total_score = 0
        ConversationHistory.objects.filter(question__test_id=test_id).delete()

        for temp_answer in temp_answers:
            partial_conditions = temp_answer.question.get_partial_conditions()
            feedback, score = grade_question(
                temp_answer.question.content,
                temp_answer.question.correct_answer,
                temp_answer.answer_text,
                temp_answer.question.score,
                partial_conditions=partial_conditions
            )
            temp_answer.is_finalized = True
            temp_answer.save()
            ConversationHistory.objects.create(
                question=temp_answer.question,
                user_answer=temp_answer.answer_text,
                feedback=feedback,
                score=score
            )
            total_score += score

        temp_answers.delete()

        test = get_object_or_404(Test, test_id=test_id)
        test.total_score = total_score  # 必要に応じて変更
        test.save()

        return redirect("studentshow_results", test_id=test_id)

# 採点結果表示画面
def show_results(request, test_id):
    """
    採点結果を表示するビュー。
    """
    test = get_object_or_404(Test, test_id=test_id)
    history = ConversationHistory.objects.filter(question__test=test)

    # 合計得点を計算
    total_score = sum(entry.score for entry in history if entry.score is not None)
    
    # 最大得点を計算（質問ごとの配点を合計）
    max_score = sum(question.score for question in test.questions.all())

    return render(request, "show_results.html", {
        "test": test,
        "history": history,
        "total_score": total_score,
        "max_score": max_score,  # 計算した最大得点
    })

# 採点基準設定画面
def set_grading_criteria(request, test_id):
    """
    試験の採点基準を設定するビュー。
    """
    test = get_object_or_404(Test, test_id=test_id)
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

# 生徒採点結果表示画面
def studentshow_results(request, test_id):
    """
    採点結果を表示するビュー。
    """
    test = get_object_or_404(Test, test_id=test_id)
    history = ConversationHistory.objects.filter(question__test=test)

    # 合計得点を計算
    total_score = sum(entry.score for entry in history if entry.score is not None)
    
    # 最大得点を計算（質問ごとの配点を合計）
    max_score = sum(question.score for question in test.questions.all())

    return render(request, "studentshow_results.html", {
        "test": test,
        "history": history,
        "total_score": total_score,
        "max_score": max_score,  # 計算した最大得点
    })

