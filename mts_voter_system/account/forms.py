from django import forms
from .models import *

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    stud_no = forms.CharField(
        required=True, 
        max_length=10, 
        label="Student Number",
        help_text="Must be 10 digits"
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'stud_no', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['password'].required = False
        else:
            self.fields['stud_no'].required = True

    def clean_stud_no(self):
        stud_no = self.cleaned_data['stud_no'].strip()
        # Proper validation for 10 digits
        if len(stud_no) != 10 or not stud_no.isdigit():
            raise forms.ValidationError("Student number must be exactly 10 digits")

        # Check uniqueness correctly
        qs = CustomUser.objects.filter(stud_no=stud_no)
        if self.instance.pk:  # For updates
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This student number is already registered")
        return stud_no

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        # Check uniqueness correctly
        qs = CustomUser.objects.filter(email=email)
        if self.instance.pk:  # For updates
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already registered")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            return self.instance.password  # For updates
        return make_password(password) 

