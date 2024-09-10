from django.contrib.auth            import login as auth_login
from django.shortcuts               import render, redirect
from apps.user.forms.forms        import SignInForm

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('swagger')
    else:
        form = SignInForm()
    return render(request, 'registration/signup.html', {'form': form})