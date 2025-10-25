from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.
def register(request):
    if request.method =="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
               messages.error(request, "Username already exist")
               return redirect('accounts:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, "You are not registered and can log in")
                return redirect('accounts:login')         
        else:
            messages.error(request, "Passwords do not match")
            return redirect('accounts:register')
        
        # print('submit') 
        # messages.success(request,"Account created successfully")
        # #debug messages content
        # #storage=messages.get_messages(request)
        # #for message in storage:
        # #   print(message.level_tag, message.message)
        # return redirect('accounts:register')
    else:    #this else, if you go to a website, you copy other people link and work in your own account however cannot as no token, so here we create a html so it can 
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == "POST":
        username=request.POST['username']  #use post so the password not shown on website when entering when press sybmit
        password = request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, "You are now logged in")
            return redirect('accounts:dashboard')           
        else:
            messages.error(request,"Invalid credentials")
            return redirect('accounts:login')
    else:    
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
    return redirect("pages:index")

def dashboard(request):
    user_contacts=Contact.objects.filter(user_id=request.user.id).order_by('-contact_date') 
    #filter user_id from table contacts where all queries info
    # add order by to force it to update the database
    # filter user_id from table contact
    # put in variable user_contacts
    context={"contacts":user_contacts} 
    return render(request, 'accounts/dashboard.html',context)
