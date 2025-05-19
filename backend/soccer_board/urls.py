"""
URL configuration for soccer_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

# urls.py
from django.contrib import admin
from django.urls import path
from django.urls import path
from users.views import UserMeView, TestUserDetailView
from board.views import (
    BoardView, BoardDetailView, BoardSaveView, SceneObjectListView, TestBoardView, TestBoardDetailView, TestBoardSaveView, TestSceneObjectView
)

urlpatterns = [
    path('api/users/me', UserMeView.as_view()),
    path('api/boards/', BoardView.as_view()),
    path('api/boards/<int:pk>', BoardDetailView.as_view()),
    path('api/boards/<int:board_id>/save', BoardSaveView.as_view()),
    path('api/scenes/<int:scene_id>/objects', SceneObjectListView.as_view()),
    path('admin/', admin.site.urls),  # Admin 페이지 접근 경로

    #테스트용
    path('api/test/users/<int:id>/', TestUserDetailView.as_view(), name='test-user-detail'),
    path('api/test/boards/<int:id>', TestBoardView.as_view()),
    path('api/test/boards/<int:user_id>/<int:board_id>', TestBoardDetailView.as_view()),
    path('api/test/boards/<int:user_id>/<int:board_id>/save', TestBoardSaveView.as_view()),
    path('api/test/scenes/<int:scene_id>/objects', TestSceneObjectView.as_view()),
    # path()
]