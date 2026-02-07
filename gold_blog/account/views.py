from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from .emailer import send_email_brevo
from .models import EmailOTP
from .utils import generate_otp, otp_expire, otp_cooldown_remaining
from .forms import UserRegistrationForm

COOLDOWN_SECONDS = 60
# Create your views here.
# registration from forms.py->views.py -> urls.py -> templates
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.is_active = False
            # save user object
            new_user.save()
            code = generate_otp()
            EmailOTP.objects.update_or_create(
                user=new_user,
                defaults={
                    'code_hash': make_password(code),
                    'expires_at': otp_expire(10),
                    'attempts': 0,
                    'last_sent_at': timezone.now(),
                }
            )

            try:
                send_email_brevo(
                    new_user.email,
                    "Your verification code",
                    f"Your code is: {code}",
                )
            except Exception:
                messages.error(
                    request,
                    "We couldn't send the verification email. Please try again later."
                )
                return render(request, 'account/register.html', {'user_form': user_form})

            request.session['pending_user_id'] = new_user.id
            return redirect('verify_email')
            

                        
            # create the user profile
            # Profile.objects.create(user=new_user)
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return render(
                request,
                'account/register.html',
                {'user_form':user_form}
            )
    else:
        user_form = UserRegistrationForm()
        return render(
            request,
            'account/register.html',
            {'user_form':user_form}
        )
        
def verify_email(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('login')
    
    user = get_user_model().objects.get(id=user_id)
    otp = EmailOTP.objects.get(user=user)
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        if otp.is_expired():
            return render(
                request,
                'account/verify.html',
                {
                    'error': 'Code expired'
                }
            )
        if otp.attempts >=5:
            return render(
                request,
                'account/verify.html',
                {'error': 'To many attempts.'}
            )
        if check_password(code, otp.code_hash):
            user.is_active = True
            user.save()
            otp.delete()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect('blog:post_list')
        
        otp.attempts +=1
        otp.save()
        return render(request, 'account/verify.html', {'error': 'Wrond code.'})
    return render(request, 'account/verify.html')

@require_POST
def resend_otp(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('login')
    
    user = get_user_model().objects.get(id=user_id)
    otp = EmailOTP.objects.get(user=user)
    
    remaining = otp_cooldown_remaining(otp.last_sent_at, seconds= COOLDOWN_SECONDS)
    if remaining > 0:
        return render(
            request,
            'account/verify.html',
            {'error': f'Please wait {remaining}s before requestion a new code.'}
        )
        
    code = generate_otp()
    otp.code_hash = make_password(code)
    otp.expires_at = otp_expire(10)
    otp.attempts = 0
    otp.last_sent_at = timezone.now()
    otp.save()
    send_email_brevo(user.email, "Your verification code", f"Your code is: {code}")

    return render(
                    request,
                  'account/verify.html', 
                  {'info': 'New code sent.'}
                )
            
