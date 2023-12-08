from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    
    subject = models.CharField(max_length=200)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content = models.TextField()

    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
    
    
class Answer(models.Model):
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content = models.TextField()

    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer of Question{self.question.id}('{self.question.subject}')"

