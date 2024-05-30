from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
import datetime

date = datetime.datetime.now().year
date1=datetime.datetime.now()
@login_required(login_url='log_in')
def index(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save to the database
        student = Student(name=name, email=email, phone=phone, message=message)
        student.save()

        # Prepare email content
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
            'date1':date1
        }
        
        # Render HTML email content
        html_content = render_to_string('msg.html', context)
        
        # Create plain text version
        plain_content = strip_tags(html_content)

        # Create the email
        subject = "Thank You for Contacting Us!"
        from_email = 'kingstonboysagar@gmail.com'
        recipient_list = [email]

        # Use EmailMultiAlternatives to send multi-part email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_content,  # The plain text part
            from_email=from_email,
            to=recipient_list,
        )

        # Attach HTML content
        email.attach_alternative(html_content, "text/html")

        # Send the email
        email.send(fail_silently=False)

        # Show a success message to the user
        messages.success(request, f"Hi {name}, thanks for contacting us! Please check your email for confirmation.")

        # Redirect back to index
        return redirect('index')

    # Render the index page
    return render(request, 'index.html', {'date': date})

@login_required(login_url='log_in')
def about(request):
    return render(request,'about.html',{'date':date})

@login_required(login_url='log_in')
def contact(request):
    return render(request,'contact.html',{'date':date})

@login_required(login_url='log_in')
def menu(request):
    return render(request,'menu.html',{'date':date})

@login_required(login_url='log_in')
def service(request):
    return render(request,'services.html',{'date':date})

def register(request):
    if request.method=='POST':
        name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,f"Hello {name} your username is already exists")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,f"Hello {name} your email is already exists!!")
                return redirect("register")
            else:
                User.objects.create_user(first_name=name,username=username,email=email,password=password)
                messages.success(request,f" Hello {name} you have register successfully")
        else:
            messages.error(request,"password doesn't match!!")
    return render(request,'auth/register.html')
def log_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not found")
            return redirect('log_in')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')    
    return render(request,'auth/login.html')

def  log_out(request):
    logout(request)
    return redirect('log_in')