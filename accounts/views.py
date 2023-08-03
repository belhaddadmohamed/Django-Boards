from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

#Create your views here.

def signup(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():    
            user = form.save()
            auth_login(request, user)

            return redirect('home')    

    return render(request, 'signup.html', {'form':form})


#update account information
class UpdateAccountView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = "my_account.html"
    success_url = reverse_lazy("my_account")

    # get the current object from the database istead of using "pk_url_kwarg" => because we don't have pk passed in th UrL
    def get_object(self):
        return self.request.user




# by default
# def signup(request):
#     form = UserCreationForm()

#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():    
#             user = form.save()
#             auth_login(request, user)

#             return redirect('home')    

#     return render(request, 'signup.html', {'form':form})