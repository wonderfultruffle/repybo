from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from ..models import Question, Answer

class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User()
        cls.user.save()

        cls.question = Question(subject="answer test", content="no question", author=cls.user)
        cls.question.save()

        cls.answer = Answer(content="no answer", question=cls.question, author=cls.user)
        cls.answer.save()


    def test_question(self):

        expected_str = f"{ModelTest.question.id}({ModelTest.question.subject})"
        self.assertEqual(expected_str, ModelTest.question.__str__())


    def test_answer_str(self):

        expected_str = f"Answer_{ModelTest.answer.id} of Question_{ModelTest.question.id}('{ModelTest.question.subject}')"
        self.assertEqual(expected_str, ModelTest.answer.__str__())

