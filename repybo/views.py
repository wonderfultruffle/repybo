from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

# Create your views here.
def index(request):
    page = request.GET.get("page", "1")
    question_list = Question.objects.order_by("-created_date")

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {"question_list": page_obj}
    return render(request, "repybo/question_list.html", context)


######## generic view 연습
# from django.views import generic
#
# class IndexView(generic.ListView):
#     def get_queryset(self):
#         return Question.objects.order_by("-create_date")
#
# class DetailView(generic.DetailView):
#     model = Question



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    context = {"question": question}
    return render(request, "repybo/question_detail.html", context)


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

