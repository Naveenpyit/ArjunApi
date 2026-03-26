from django.urls import path
from . import views

urlpatterns = [
    path('users/',views.UserViews.as_view()),
    path('users/<int:pk>/',views.UserViews.as_view()),

    # auth
    path('auth/login/',views.LoginView.as_view()),
    path('auth/currentuser/',views.CurrentUser.as_view()),
    path('auth/refresh/',views.RefreshTokenView.as_view()),
    path('auth/logout/',views.LogoutView.as_view()),
]