from django.shortcuts import render, redirect

# Create your views here.
from .form import CreateUserForms

def register(request):
    
    form = CreateUserForms()
    
    if request.method == 'POST':
        form = CreateUserForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        
    
    
    context = {'form':form}
    
    return render(request, 'account/registration/register.html', context=context)