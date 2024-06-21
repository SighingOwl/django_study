from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    # pybo 목록 출력

    # 입력 인자
    page = request.GET.get('page', '1') # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date')
                                 
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지 당 질문 10개씩 표시
    page_obj = paginator.get_page(page)
    
    context = {'question_list' : page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # pybo 질문 내용 출력
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    # pybo 답변 등록
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.auther = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        # request.method가 GET인 경우
        form = AnswerForm()

    context = {'question': question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)

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
            return redirect('pybo:detail', question_id=answer.question.id)
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