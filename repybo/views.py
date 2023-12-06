from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator

from .models import Question
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


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # question.answer_set.create(content=request.POST.get("content"))
    #
    # return redirect("pybo:detail", question_id=question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        return HttpResponseNotAllowed("Only POST is allowed.")


def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pybo:index")
    else:
        form = QuestionForm()

    context = {"form": form}
    return render(request, "repybo/question_form.html", context)