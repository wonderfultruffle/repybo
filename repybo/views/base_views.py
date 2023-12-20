from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
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
    cname_vst_q = "ck_vst"
    cval_vst_q = request.COOKIES.get(cname_vst_q, f"{request.user.username}_")

    if request.user == question.author:
        pass
    else:
        if cval_vst_q.__contains__(request.user.username) and cval_vst_q.__contains__(f"{question_id}-"):
            pass
        else:
            if not cval_vst_q.__contains__(f"{question_id}-"):
                cval_vst_q += f"{question_id},"

            question.views += 1
            question.save()

    context = {"question": question}
    response = render(request, "repybo/question_detail.html", context)

    if cval_vst_q:
        response.set_cookie(cname_vst_q, cval_vst_q)

    return response


######## generic view 연습
# from django.views import generic
#
# class IndexView(generic.ListView):
#     def get_queryset(self):
#         return Question.objects.order_by("-create_date")
#
# class DetailView(generic.DetailView):
#     model = Question
