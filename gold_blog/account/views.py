from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib import messages
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
            # save user object
            new_user.save()
            # create the user profile
            # Profile.objects.create(user=new_user)
            return render(
                request,
                'account/register_done.html',
                {'new_user':new_user}
            )
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