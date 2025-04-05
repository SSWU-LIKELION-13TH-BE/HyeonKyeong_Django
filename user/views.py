from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm



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
    return render(request, 'home.html')

def index_view(request):
    context = {
        'title': 'User list',
        'user_list' : [
            {'no': 1, 'title': '목록1'},
            {'no': 2, 'title': '목록2'},
            {'no': 3, 'title': '목록3'},
            {'no': 4, 'title': '목록4'},
            {'no': 5, 'title': '목록5'}
        ]
    }
    return render(request, 'user/index.html', context)

def user_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_view')  # url name에 맞게 조정
    else:
        form = UserForm()

    users = User.objects.all()
    context = {
        'boardForm': form,
        'users': users,
    }
    return render(request, 'board.html', context)