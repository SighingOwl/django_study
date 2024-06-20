from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

def signup(request):
    # 회원가입
    # POST 요청일 때 입력된 데이터로 사용자 생성
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    # GET 요청일 때 회원가입 페이지를 표시    
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
