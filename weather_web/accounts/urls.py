from django.urls import path
from django.contrib.auth import views as auth_views
from .views import GoodbyeView, login_view, logout_view, sign_up_view, user_preference_update_view, password_change

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view,
         name='logout'),
    path('signup/', sign_up_view, name='signup'),
    path('goodbye/', GoodbyeView.as_view(), name='goodbye'),
    path('edit/', user_preference_update_view, name='edit'),
    path('edit_password/', password_change, name='edit_password'),
]
