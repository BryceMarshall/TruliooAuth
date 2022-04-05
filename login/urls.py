from django.urls import path

from login import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login-view'),
    path('logout/', views.LogoutView.as_view(), name='logout-view'),
    path('register/', views.RegisterView.as_view(), name='register-view'),
    path('home/', views.HomeView.as_view(), name='home-view')

]
