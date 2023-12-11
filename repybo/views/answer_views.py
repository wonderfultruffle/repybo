from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question, Answer
from ..forms import AnswerForm

@login_required(login_url="common:login")
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = AnswerForm()

    context = {"question": question, "form": form}
    return render(request, "repybo/question_detail.html", context)


@login_required(login_url="common:login")
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question_id = answer.question.id

    if request.user != answer.author:
        messages.error(request, "답변 수정 권한이 없습니다.")
        return redirect("pybo:detail", question_id)

    if request.method=="POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect("pybo:detail", question_id)
    else:
        form = AnswerForm(instance=answer)

    context={"question":answer.question, "answer":answer, "form":form}
    return render(request, "repybo/question_detail.html", context)


@login_required(login_url="common:login")
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect("pybo:detail", answer.question.id)

    answer.delete()
    return redirect("pybo:detail", answer.question.id)


@login_required(login_url="common:login")
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        messages.error(request, "자신의 글은 추천할 수 없습니다.")
    else:
        answer.voter.add(request.user)

    return redirect("pybo:detail", question_id=answer.question.id)