from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from ..models import Question, Answer

class ModelTest(TestCase):

    # def setUp(self):

    def create_objects(self):
        self.user = User()
        self.user.save()

        self.question = Question(subject="answer test", content="no question", author=self.user)
        self.question.save()

        self.answer = Answer(content="no answer", question=self.question, author=self.user)
        self.answer.save()


    def test_question(self):
        self.create_objects()

        expected_str = f"{self.question.id}({self.question.subject})"
        self.assertEqual(expected_str, self.question.__str__())


    def test_answer_str(self):
        self.create_objects()

        expected_str = f"Answer_{self.answer.id} of Question_{self.question.id}('{self.question.subject}')"
        self.assertEqual(expected_str, self.answer.__str__())

