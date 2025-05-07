from django.urls import path
from .views import (
    signup_view, login_view, logout_view, home_view, board_view,
    comment_view, toggle_like_view, board_detail_view, toggle_comment_like_view,
    profile_edit_view, post_edit, post_delete, mypage_view, guestbook_view 
)
from django.contrib.auth import views as auth_views  # 비밀번호 관련 뷰를 가져옴



app_name='user'

urlpatterns = [
    path('signup/',signup_view, name='signup'),
    path("login/", login_view, name="login"),  # 로그인 URL
    path('logout/', logout_view, name='logout'),  # 로그아웃 URL 추가
    path('', home_view, name='home'),  # 홈 페이지 URL, 기본 루트 URL에 연결

  # 비밀번호 재설정 URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


  #게시판 기능 구현
  path('board/board', board_view, name = 'board' ),

  #좋아요 댓글
  path('board/<int:pk>/', board_detail_view, name='board_detail'),
  path('board/<int:pk>/comment/', comment_view, name='comment'), 
  path('board/<int:pk>/toggle_like/', toggle_like_view, name='toggle_like'), 
  path('comment/<int:comment_id>/toggle_like/', toggle_comment_like_view, name='toggle_comment_like'),
  
  path('edit/<int:pk>/', post_edit, name='post_edit'),
  path('delete/<int:pk>/', post_delete, name='post_delete'),
  path('mypage/', mypage_view, name='mypage'),
  path('profile/edit/', profile_edit_view, name='profile_edit'),

  path('guestbook/<str:username>/', guestbook_view, name='guestbook'),
]