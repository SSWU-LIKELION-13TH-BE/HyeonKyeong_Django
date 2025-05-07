from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Like, Board, Comment, CommentLike, Stack, Guestbook
from .forms import BoardForm, CommentForm, GuestbookForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from django.http import HttpResponseForbidden

from django.db.models import Q


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
    sort = request.GET.get('sort', 'latest')
    search = request.GET.get('q', '')

    board_list = Board.objects.all()

    if search:
        board_list = board_list.filter(

            Q(title__icontains=search) |
            Q(content__icontains=search)
        )

    if sort == 'latest':
        board_list = board_list.order_by('-created_at')
    elif sort == 'popular':
        board_list = board_list.order_by('-hits')

    context = {
        'board_list': board_list,
        'sort': sort,
        'search': search,
    }
    return render(request, 'home.html', context)



def board_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        writer = request.user  # 현재 로그인된 유저 객체
        stack_ids = request.POST.getlist('stacks')   #  리스트로 받기!
        github_link = request.POST.get('github_link')
        image = request.FILES.get('image')

        board = Board(
            title=title,
            content=content,
            writer=request.user,
            github_link=github_link,
            image=image,
        )
        board.save()
        stack_objs = Stack.objects.filter(id__in=stack_ids)
        board.stacks.set(stack_objs)
        return redirect('user:home')
    else:
        boardForm = BoardForm()
        board = Board.objects.all()
        stacks = Stack.objects.all()
        context = {
            'boardForm': boardForm,
            'board': board,
            'stacks': stacks,
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

    # guestbooks 조회
    guestbooks = Guestbook.objects.filter(owner=board.writer)

    cookie_name = 'hit_board'
    cookie_value = request.COOKIES.get(cookie_name, '_')

    context = {
        'board': board,
        'comment_form': comment_form,
        'guestbooks': guestbooks,
        'writer': board.writer,
    }
    response = render(request, 'board/board_detail.html', context)

    # 조회수 쿠키 조건
    if f'_{pk}_' not in cookie_value:
        cookie_value += f'{pk}_'
        expire_date = datetime.now() + timedelta(days=1)
        expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
        max_age = (expire_date - datetime.now()).total_seconds()

        board.hits += 1
        board.save()

        response.set_cookie(cookie_name, value=cookie_value, max_age=max_age, httponly=True)

    return response


def toggle_comment_like_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('user:board_detail', pk=comment.posting.id)
  
@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:mypage')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Board, pk=pk, writer=request.user)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('user:mypage')
    else:
        form = BoardForm(instance=post)
    return render(request, 'accounts/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Board, pk=pk, writer=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('user:mypage')
    return render(request, 'accounts/post_confirm_delete.html', {'post': post})

@login_required
def mypage_view(request):
    posts = Board.objects.filter(writer=request.user)
    return render(request, 'accounts/mypage.html', {'user': request.user, 'posts': posts})


@login_required
def guestbook_view(request, username):
    CustomUser = get_user_model()
    owner = get_object_or_404(CustomUser, username=username)

    if request.method == 'POST':
        form = GuestbookForm(request.POST)
        if form.is_valid():
            guestbook = form.save(commit=False)
            guestbook.owner = owner
            guestbook.writer = request.user
            guestbook.save()
            return redirect('user:guestbook', username=username)
    else:
        form = GuestbookForm()

    # 본인만 볼 수 있도록
    if request.user == owner:
        guestbooks = Guestbook.objects.filter(owner=owner)
    else:
        guestbooks = None

    return render(request, 'accounts/guestbook.html', {
        'form': form,
        'guestbooks': guestbooks,
        'owner': owner,
    })

