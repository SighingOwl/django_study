from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..models import Question, Answer
from ..forms import AnswerForm

@login_required(login_url='common:login')
def answer_create(request, question_id):
    # pybo 답변 등록
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        # request.method가 GET인 경우
        form = AnswerForm()

    context = {'question': question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    # pybo 답변 수정

    answer = get_object_or_404(Answer, pk=answer_id)
    # 요청자와 답변 작성자가 다를 때 수정 거부
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)
    
    # 요청 메소드가 POST일 때 입력된 수정 답변을 answer 모델에 저장
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    # 요청 메소드가 GET일 때 기존의 답변 데이터를 가져와 폼을 생성
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    # pybo 답변 삭제
    answer = get_object_or_404(Answer, pk=answer_id)
    
    # 삭제 요청자와 답변 작성자가 다를 때 삭제 거부
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    # 삭제 요청자와 답변 작성자가 같을 때 삭제
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question_id)