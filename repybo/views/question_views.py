from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question
from ..forms import QuestionForm

@login_required(login_url="common:login")
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect("pybo:index")
    else:
        form = QuestionForm()

    context = {"form": form}
    return render(request, "repybo/question_form.html", context)

@login_required(login_url="common:login")
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "질문 수정 권한이 없습니다.")
        return redirect("pybo:detail", question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)

    context = {"form": form}
    return render(request, "repybo/question_form.html", context)


@login_required(login_url="common:login")
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect("pybo:detail", question.id)

    question.delete()
    return redirect("pybo:index")


@login_required(login_url="common:login")
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        messages.error(request, "자신의 글은 추천할 수 없습니다.")
    else:
        question.voter.add(request.user)

    return redirect("pybo:detail", question_id=question.id)


def question_cancel_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user in question.voter.all():
        question.voter.remove(request.user)

    return redirect("pybo:detail", question_id=question.id)
