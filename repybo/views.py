from django.shortcuts import render, get_object_or_404

from .models import Question

# Create your views here.
def index(request):
    question_list = Question.objects.order_by("-create_date")

    context = {"question_list": question_list}

    return render(request, "repybo/question_list.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

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
