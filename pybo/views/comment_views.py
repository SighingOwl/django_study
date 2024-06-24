from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question, Answer, Comment
from ..forms import CommentForm

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    # pybo 질문 댓글 등록
    question = get_object_or_404(Question, pk=question_id)
    
    # 요청 메소드가 POST일 때 입력된 댓글 데이터를 comment 모델에 저장
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    # 요청 메소드가 GET일 때 댓글폼을 로드
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    # pybo 질문 댓글 수정
    comment = get_object_or_404(Comment, pk=comment_id)

    # 수정 요청자와 작성자가 다르면 댓글 수정 거부
    if request.user != comment.author:
        messages.error(request, '댓글수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question.id)
    
    # 요청 메소드가 POST일 때 입력된 댓글 데이터로 기존 댓글을 변경
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    # 요청 메소드가 GET일 때 기존 댓글을 포함한 댓글폼을 생성
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    # pybo 질문 댓글 삭제
    comment = get_object_or_404(Comment, pk=comment_id)

    # 삭제 요청자와 작성자가 다르면 댓글 삭제 거부
    if request.user != comment.author:
        messages.error(request, '댓글삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question.id)
    # 삭제 요청자와 작성자가 같으면 댓글 삭제
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)

@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    # pybo 답변 댓글 등록
    answer = get_object_or_404(Answer, pk=answer_id)
    
    # 요청 메소드가 POST일 때 입력된 댓글 데이터를 comment 모델에 저장
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    # 요청 메소드가 GET일 때 댓글폼을 로드
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    # pybo 답변 댓글 수정
    comment = get_object_or_404(Comment, pk=comment_id)

    # 수정 요청자와 작성자가 다르면 댓글 수정 거부
    if request.user != comment.author:
        messages.error(request, '댓글수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    
    # 요청 메소드가 POST일 때 입력된 댓글 데이터로 기존 댓글을 변경
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    # 요청 메소드가 GET일 때 기존 댓글을 포함한 댓글폼을 생성
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    # pybo 답변 댓글 삭제
    comment = get_object_or_404(Comment, pk=comment_id)

    # 삭제 요청자와 작성자가 다르면 댓글 삭제 거부
    if request.user != comment.author:
        messages.error(request, '댓글삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    # 삭제 요청자와 작성자가 같으면 댓글 삭제
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)