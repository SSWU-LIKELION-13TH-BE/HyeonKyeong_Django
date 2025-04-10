from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Like, Board, Comment, CommentLike
from .forms import BoardForm, CommentForm
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')
        else:
            print(form.errors) 
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

#댓글작성
def comment_view(request, pk):
    posting = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent = Comment.objects.get(id=parent_id) if parent_id else None
            Comment.objects.create(
                user=request.user,
                posting=posting,
                content=form.cleaned_data['content'],
                parent=parent
            )
    return redirect('user:board_detail', pk=pk)


@login_required(login_url='login')  # 로그인하지 않은 경우 로그인 페이지로 이동
def toggle_like_view(request, pk):
    comment = get_object_or_404(Board, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, posting=comment)
    if not created:
        like.delete()
    return redirect('user:board_detail', pk=pk)
    
def board_detail_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    comment_form = CommentForm()
    return render(request, 'board/board_detail.html', {
        'board': board,
        'comment_form': comment_form,
    })

def toggle_comment_like_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('user:board_detail', pk=comment.posting.id)