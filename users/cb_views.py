from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from users.forms import SignupForm, LoginForm
from utils.email import send_email


User = get_user_model()

class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save()

        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        url = f"{self.request.scheme}://{self.request.META['HTTP_HOST']}/users/verify/?code={signer_dump}"
        subject = f"[Todo]{user.email}의 이메일 인증 링크"
        message = f"링크를 클릭해 이메일 인증 \n{url}"
        send_email(subject=subject, message=message, from_email=None, to_email=user.email)

        return render(self.request, "signup_done.html", {"user": user})

def verify_email(request):
    code = request.GET.get('code')

    signer = TimestampSigner()
    try:
        decoded_user_email = signer.unsign(code)
        user_email = signer.unsign(decoded_user_email, max_age=60 * 5)
    except (TypeError, SignatureExpired):
        return render(request, 'verify_failed.html')

    user = get_object_or_404(User, email=user_email)
    user.is_active = True
    user.save()
    return render(request, 'verify_success.html')

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy("cbv_todo_list")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())