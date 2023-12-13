from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from ..models import Question, Answer
from ..views.base_views import index, detail

# Create your tests here.
class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_questions = 15
        author = User()
        author.save()

        for i in range(number_of_questions):
            Question.objects.create(author=author, subject=f"Question[{i}]", content="no data.")


    def test_index_view_accessible_by_name(self):
        response = self.client.get(reverse("pybo:index"))
        self.assertEqual(response.status_code, 200)


    def test_root_url_resolves_index_view(self):
        found = resolve("/")
        self.assertEqual(found.func, index)


    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse("pybo:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "repybo/question_list.html")


    def test_index_view_pagination_is_ten(self):
        response = self.client.get(reverse("pybo:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("question_list" in response.context)
        self.assertEqual(response.context["question_list"].paginator.per_page, 10)
        self.assertEqual(len(response.context["question_list"]), 10)


class DetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_questions = 15
        author = User()
        author.save()

        for i in range(number_of_questions):
            Question.objects.create(author=author, subject=f"Question[{i}]", content="Detail view test.")


    def test_detail_view_accessible_by_name(self):
        question_count = len(Question.objects.all())

        for question_num in range(1, question_count+1):
            response = self.client.get(reverse("pybo:detail", args=[question_num]))
            self.assertEqual(response.status_code, 200)


    def test_question_id_url_resolves_detail_view(self):
        question_count = len(Question.objects.all())

        for question_num in range(1, question_count+1):
            found = resolve(f"/{question_num}/", urlconf="repybo.urls")
            self.assertEqual(found.func, detail)


    def test_detail_view_uses_correct_template(self):
        question_count = len(Question.objects.all())

        for q_id in range(1, question_count+1):
            response = self.client.get(reverse("pybo:detail", args=[q_id]))
            self.assertEqual(response.status_code, 200)

            self.assertTemplateUsed(response, "repybo/question_detail.html")
