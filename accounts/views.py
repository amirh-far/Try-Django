from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect("/login/")
    
    context = {"form": form}
    return render(request, "accounts/register.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return render(request, "accounts/already-loged-in.html", {})
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {"error": "Invalid Username or Password"}
            return render(request, "accounts/login.html", context=context)
        print(user)
        login(request, user)
        return redirect("/admin/")
    return render(request, "accounts/login.html", {})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "accounts/logout.html", {})

    
