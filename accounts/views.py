from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import LoginForm, RegistrationForm, VerificationCodeForm, CompleteRegistrationForm
from .models import EmailVerificationCode


def login_view(request):
    """
    Handle user login
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Check if username is actually an email
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    pass
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'欢迎回来，{user.username}！')
                
                # Redirect to the page user was trying to access, or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
        else:
            messages.error(request, '登录失败，请检查用户名和密码')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    messages.info(request, '您已成功退出登录')
    return redirect('/')


def register_step1(request):
    """
    Step 1 of registration: Email verification
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            # Generate verification code
            verification = EmailVerificationCode.generate_code(email)
            
            # Send verification email
            send_verification_email(email, verification.code)
            
            # Redirect to verification page
            return redirect(reverse('accounts:verify_email') + f'?email={email}')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register_step1.html', {'form': form})


def verify_email(request):
    """
    Step 2 of registration: Verify email with code
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    email = request.GET.get('email', '')
    if not email:
        return redirect('register')
    
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        form.initial = {'email': email}
        
        if form.is_valid():
            # Mark verification code as used
            verification = EmailVerificationCode.objects.get(email=email)
            verification.is_used = True
            verification.save()
            
            # Redirect to complete registration
            return redirect(reverse('accounts:complete_registration') + f'?email={email}')
    else:
        form = VerificationCodeForm(initial={'email': email})
    
    return render(request, 'accounts/verify_email.html', {'form': form, 'email': email})


def complete_registration(request):
    """
    Step 3 of registration: Complete user registration
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    email = request.GET.get('email', '')
    if not email:
        return redirect('register')
    
    # Check if email was verified
    verification = EmailVerificationCode.objects.filter(email=email, is_used=True).first()
    if not verification:
        messages.error(request, '请先验证您的邮箱')
        return redirect('register')
    
    if request.method == 'POST':
        # Add email to POST data
        post_data = request.POST.copy()
        post_data['email'] = email
        form = CompleteRegistrationForm(post_data)
        
        if form.is_valid():
            # Save the user with proper password hashing
            user = form.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, f'注册成功！欢迎加入，{user.username}！')
            return redirect('/')
    else:
        form = CompleteRegistrationForm(initial={'email': email})
    
    return render(request, 'accounts/complete_registration.html', {'form': form})


@require_POST
def resend_verification(request):
    """
    Resend verification code
    """
    email = request.POST.get('email', '')
    if not email:
        return JsonResponse({'success': False, 'message': '邮箱不能为空'})
    
    # Generate new verification code
    verification = EmailVerificationCode.generate_code(email)
    
    # Send verification email
    send_verification_email(email, verification.code)
    
    return JsonResponse({'success': True, 'message': '验证码已重新发送'})


def send_verification_email(email, code):
    """
    Send verification email with code
    """
    subject = '招聘导航网站 - 邮箱验证码'
    message = f'''
    您好，

    感谢您注册招聘导航网站。您的邮箱验证码是：

    {code}

    该验证码将在10分钟内有效。

    如果您没有注册我们的网站，请忽略此邮件。

    祝好，
    招聘导航网站团队
    '''
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
