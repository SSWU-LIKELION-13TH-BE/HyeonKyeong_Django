from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Board
from .forms import BoardForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user:home")  

    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "logout.html")

def home_view(request):
    board = Board.objects.all().order_by('-id')  # 최신 글부터 보여줌
    context = {
        'board': board,
    }
    return render(request, 'home.html', context)


def board_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        writer = request.POST.get('writer')
        stacks = request.POST.get('stacks')
        github_link = request.POST.get('github_link')
        image = request.FILES.get('image')

        board = Board(
            title=title,
            content=content,
            writer=writer,
            stacks=stacks,
            github_link=github_link,
            image=image,
        )
        board.save()
        return redirect('user:home')
    else:
        boardForm = BoardForm()
        board = Board.objects.all()
        context = {
            'boardForm': boardForm,
            'board': board,
        }
        return render(request, 'board/board.html', context)