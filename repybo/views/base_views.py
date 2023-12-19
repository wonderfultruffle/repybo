from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from ..models import Question


def index(request):
    page = request.GET.get("page", "1")
    kw = request.GET.get("kw", '')

    question_list = Question.objects.order_by("-create_date")

    if kw:
        question_list = question_list.filter(Q(subject__icontains=kw)|Q(content__icontains=kw)|
                                             Q(author__username__icontains=kw)|Q(answer__content__icontains=kw)|
                                             Q(answer__author__username__icontains=kw)).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {"question_list": page_obj, "page": page, "kw": kw}
    return render(request, "repybo/question_list.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        question.views += 1
        question.save()

    context = {"question": question}
    return render(request, "repybo/question_detail.html", context)


######## generic view 연습
# from django.views import generic
#
# class IndexView(generic.ListView):
#     def get_queryset(self):
#         return Question.objects.order_by("-create_date")
#
# class DetailView(generic.DetailView):
#     model = Question
