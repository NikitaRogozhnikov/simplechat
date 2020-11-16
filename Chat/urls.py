from django.urls import path
from . import views
app_name = 'Chat'
urlpatterns = [
    path('', views.MainPage.as_view(), name='main'), 
    path('register', views.RegisterView.as_view(), name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path('logout',views.logout_user,name='logout'),
    path('<int:room_name>',views.StartChating.as_view(),name='room'),
]