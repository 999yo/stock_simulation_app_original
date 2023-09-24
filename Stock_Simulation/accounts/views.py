from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import SignupForm, LoginForm, DeleteAccountForm
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

class SignupView(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_view') 
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('home')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class UserView(View):
    def get(self, request):
        user = request.user
        return render(request, 'accounts/info.html', {'user': user})
    

User = get_user_model()

@method_decorator(login_required, name='dispatch')
class DeleteAccountView(View):
    template_name = 'accounts/delete_account.html'

    def get(self, request):
        # ユーザーにパスワードを入力するフォームを表示
        form = DeleteAccountForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            # パスワードが正しいかチェック
            if request.user.check_password(password):
                # パスワードが正しい場合、ユーザーを削除
                request.user.delete()
                logout(request)  # ユーザーをログアウトさせる
                return redirect('home')  # 削除後にリダイレクトするURLを指定
            else:
                # パスワードが正しくない場合のエラーメッセージ
                form.add_error('password', 'パスワードが正しくありません。')
        
        return render(request, self.template_name, {'form': form})