from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question
from ..forms import QuestionForm

@login_required(login_url='common:login')
def question_create(request):
    # pybo 질문 등록
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        # request.method가 GET인 경우
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', {'form': form})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    # pybo 질문 수정

    question = get_object_or_404(Question, pk=question_id)
    
    # 요청자와 작성자가 다를 때 권한 없음을 알리고 질문 수정을 요청한 질문 페이지로 돌아간다.
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    
    # 요청이 POST일 때
        # 폼에 입력된 값이 유효할 때 내용과 작성자, 수정일시를 모델에 저장하고 질문 상세 페이지로 돌아간다.
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    # 요청이 GET 일 때 질문 작성 폽을 form 변수에 저장
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    # pybo 질문 삭제
    
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    question.delete()
    return redirect('pybo:index')
