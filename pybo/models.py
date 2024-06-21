from django.contrib.auth.models import User
from django.db import models

# 질문 모델
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

# 답변 모델
    # 질문에 대한 답변이 필요하므로 question은 Question 모델에서 외래키로 가져온다.
    # question은 삭제되면 질문도 함께 삭제되도록 삭제 옵션은 CASCADE로 설정
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)