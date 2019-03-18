from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.

# Register User
def register(request):
    if request.method == "POST":
        # register user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']

        # Password checking
        if password == confirm_password:
            # checking duplicate user_name
            if User.objects.filter(username = user_name).exists():
                messages.error(request, 'Username is not available!!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is being used.!!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=user_name, password=password, email=email,
                    first_name=first_name, last_name=last_name)

                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'Login Success !')
                    # return redirect('index')

                    user.save();
                    messages.success(request, 'Registration Successful!!')
                    return redirect('login')
        else:
            # error message
            messages.error(request, 'Password not matched')
            return redirect('register')

    return render(request, 'accounts/register.html')

def login(request):
    if request.method == "POST":
        # Login user
        user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=user_name, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login Success.!')
            return redirect('dashboard')
        else:
            messages.error(request, 'User not found!!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'Logout Seccess !!')
        
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    
    context = {
        'contacts': user_contacts,
    }
    return render(request, 'accounts/dashboard.html', context)