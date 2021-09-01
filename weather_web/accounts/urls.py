from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUp, GoodbyeView, login_view, logout_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view,
         name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('goodbye/', GoodbyeView.as_view(), name='goodbye')
]
