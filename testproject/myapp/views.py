from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout

# Create your views here.
def index(request):
    id = '001'
    name = 'boss'
    email = 'boss@gmail.com'
    return render(request, 'index.html',{
        'id': id,
        'name': name,
        'email': email
        }
    )

def home(request, id):
    return HttpResponse('Hello World =' + str(id))

def article(request, year, slug):
    return HttpResponse('Year =' + str(year) + 'Slug =' + slug)

def Login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book:index')
    else:
        form = AuthenticationForm()
    return render(request , 'account/login.html', {
        'form': form
    })

def Logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('myapp:index')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data= request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book:index')
    else:
        form = UserCreationForm()
    return render(request , 'account/signup.html', {
        'form': form
    })