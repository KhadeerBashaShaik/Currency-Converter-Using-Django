import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from forex_python.converter import CurrencyRates
from home.models import Contact
from django.contrib import messages

cr = CurrencyRates()

# password for test user is Harry$$$***000
# Create your views here.
def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("/login") 
    return render(request, 'index.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")


def about(request):
    return render(request, "about.html")

def input(request):
    return render(request , "input.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.date.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')

def result(request):
    if request.method == "POST":
        fr = request.POST.get('from')
        to = request.POST.get('to')
        a = request.POST.get('amount')
        r=cr.convert(fr,to,int(a))
        return render(request, "result.html", {"res":r,"fr":fr,"to":to,"a":a})

from .forms import CreateUserForm
def registerPage(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user =  form.cleaned_data.get('username')
            
            return redirect('login')

    context={'form':form}
    return render(request,'register.html',context)