from django.shortcuts import render, redirect, reverse
from .email_backend import EmailBackend
from django.contrib import messages
from .models import ApprovedStudent, CustomUser
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout,authenticate
# Create your views here.


def account_login(request):
    if request.method == 'POST':
        stud_no = request.POST.get('stud_no', '').strip()  # Clean input
        password = request.POST.get('password', '')
        print(f"Login attempt - Stud No: {stud_no}, Password: {password}")  # Debug
        
        backend = EmailBackend()
        user = backend.authenticate(request=request, username=stud_no, password=password)
        print(f"Authenticated User: {user}")  # Debug
        
        if user is not None:
            login(request, user)
            print(f"Session Key: {request.session.session_key}")
            print(f"User logged in successfully: {user}")
            # return redirect("adminDashboard" if user.user_type == '1' else "voterDashboard")
            if user.user_type == "1":
                return render(request, "admin/home.html")
            return render(request, "voting/voter/ballot.html")
        else:
            messages.error(request, "Invalid credentials")
            print("Authentication failed")
            return redirect('account_login')
    return render(request, "voting/login.html")

def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': voterForm
    }

    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            student_number = userForm.cleaned_data.get('stud_no')  # Get the student number from the form

            # Check if the student number is approved
            if not ApprovedStudent.objects.filter(student_number=student_number).exists():
                messages.error(request, "Your student number is not authorized to register.")
                return render(request, "voting/reg.html", context)

            # Check if the student number is already registered
            if CustomUser.objects.filter(stud_no=student_number).exists():
                messages.error(request, "This student number is already registered.")
                return render(request, "voting/reg.html", context)

            # Proceed with registration if the student number is approved and not already registered
            user = userForm.save(commit=False)
            user.save()
            voter = voterForm.save(commit=False)
            voter.admin = user
            voter.save()
            messages.success(request, "Account created. You can login now!")
            return redirect(reverse('voterDashboard'))
        else:
            messages.error(request, "Provided data failed validation")
            print("User Form Errors:", userForm.errors)
            print("Voter Form Errors:", voterForm.errors)
            return render(request, "voting/reg.html", context)

    return render(request, "voting/reg.html", context)

def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))
