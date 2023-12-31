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
    cval_vst_q = request.COOKIES.get(cname_vst_q, '')
    if request.user == question.author:  # 현재 사용자가 질문 작성자일 때 skip
        pass
    else:
        # Cookie 생성
        ### 익명 사용자 방문 이력 cookie 가 존재하지 않을 때
        if len(request.user.username) == 0 and cval_vst_q[:7] != "visited":
            cval_vst_q = f"visited: "

        ### 현재 사용자의 cookie 가 존재하지 않을 때
        elif not (cval_vst_q and cval_vst_q.__contains__(request.user.username)):
            cval_vst_q = f"{request.user.username}_visited: "

        # 방문 이력이 없을 때 조회수 증가
        if not cval_vst_q.__contains__(f"{question_id},"):
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
