from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password==cpassword:
                if User.objects.filter(username=username).exists():
                     messages.info(request,"username already taken")
                     return redirect('/')
                elif User.objects.filter(email=email).exists():
                   messages.info(request,"email already taken")
                   return redirect('/')
                else:

                    user=User.objects.create_user(username=username,first_name=firstname,password=password,email=email,last_name=lastname)
                    user.save();
                    print("user created")
        else:
                messages.info(request,"password not maching")
                return redirect('register')
        return redirect('login')


    return render(request,"register.html")

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('cartapp:allprodcat')
        else:
            messages.info(request,"incorrect username or password")
            return redirect('/')

    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')