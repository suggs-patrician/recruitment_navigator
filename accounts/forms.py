from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import EmailVerificationCode


class LoginForm(AuthenticationForm):
    """
    Custom login form with styled fields
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名或邮箱'}),
        label='用户名或邮箱'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
        label='密码'
    )


class RegistrationForm(forms.Form):
    """
    Step 1 of registration: Email verification
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入您的邮箱'}),
        label='邮箱',
        required=True
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('该邮箱已被注册，请使用其他邮箱或找回密码')
        return email


class VerificationCodeForm(forms.Form):
    """
    Step 2 of registration: Verify email with code
    """
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入6位验证码'}),
        label='验证码',
        max_length=6,
        min_length=6,
        required=True
    )
    email = forms.EmailField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        email = cleaned_data.get('email')

        if code and email:
            verification = EmailVerificationCode.objects.filter(email=email).first()
            if not verification:
                raise ValidationError('验证码无效，请重新获取')
            
            if not verification.is_valid():
                raise ValidationError('验证码已过期，请重新获取')
            
            if verification.code != code:
                raise ValidationError('验证码错误，请重新输入')
        
        return cleaned_data


class CompleteRegistrationForm(UserCreationForm):
    """
    Step 3 of registration: Complete user registration
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请设置用户名'}),
        label='用户名',
        max_length=150,
        help_text='用户名只能包含字母、数字和 @/./+/-/_ 字符'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请设置密码'}),
        label='密码',
        help_text='密码至少需要8个字符，不能是纯数字，不能与用户名太相似'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}),
        label='确认密码',
        help_text='请再次输入相同的密码进行确认'
    )
    email = forms.EmailField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('该用户名已被使用，请选择其他用户名')
        return username