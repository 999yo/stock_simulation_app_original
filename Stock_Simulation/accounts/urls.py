from django.urls import path
from .views import SignupView, LoginView, LogoutView, UserView, DeleteAccountView
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user_view'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    
    ]
