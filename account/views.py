from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.
from .form import CreateUserForms

from django.contrib.sites.shortcuts import get_current_site

from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

def register(request):
    form = CreateUserForms()

    if request.method == 'POST':
        form = CreateUserForms(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = user_tokenizer_generate.make_token(user)
            verification_url = reverse('email-verification', kwargs={'uidb64': uid, 'token': token})
            full_verification_url = f"http://{current_site.domain}{verification_url}"

            subject = 'Account verification email'
            message = render_to_string('account/registration/email-verification.html', {
                'user': user,
                'verification_url': full_verification_url,
            })

            # Gửi email với định dạng HTML
            email = EmailMultiAlternatives(subject=subject, body=message, to=[user.email])
            email.attach_alternative(message, "text/html")
            email.send()

            return redirect('email-verification-sent')

    context = {'form': form}
    return render(request, 'account/registration/register.html', context=context)

def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    
    else:
        return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')




def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')





def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')