from django.contrib.auth.models import User
from django.db import models

# 질문 모델
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject

# 답변 모델
    # 질문에 대한 답변이 필요하므로 question은 Question 모델에서 외래키로 가져온다.
    # question은 삭제되면 질문도 함께 삭제되도록 삭제 옵션은 CASCADE로 설정
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

# 댓글 모델
    # 작성자, 내용, 작성일시, 수정일시 필드를 포함한다.
    # 댓글은 질문이나 답변에 모두 작성할 수 있으므로 질문과 답변 필드를 외래키로 가져온다.
        # 질문이나 답변 중 하나를 택해 작성하므로 질문 필드 혹은 답변 필드가 채워지지 않을 수 있어 null과 blank를 true로 둔다
        # 작성자 계정이 삭제되면 댓글도 함께 삭제되도록 한다.
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)