from django import forms
from .models import User, Course
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from dashboard.models import BookedCourse

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        exclude = ['enroll_number']
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone', 'gender',
            'dob', 'profile_picture', 'role', 'password'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")

        return cleaned_data

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=[
            "name",
            "description",
            "category",
            "fees",
            "duration",
            "trainers",
            "timing"
        ]
        widgets = {
    'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Name'}),
    'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Course Description', 'rows': 3}),
    'category': forms.TextInput(attrs={'class': 'form-control'}),
    'trainers': forms.SelectMultiple(attrs={'class': 'form-select select2'}),
    'fees': forms.NumberInput(attrs={'class': 'form-control'}),
    'duration': forms.TextInput(attrs={'class': 'form-control'}),
    'timing': forms.TextInput(attrs={'class': 'form-control'}),
}
            

        
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['trainers'].queryset = User.objects.filter(role='staff')



class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
          label='Username',
             widget=forms.TextInput(attrs={
            'class': 'form-control','id':'usernames'}
           ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'enter your password'}
    ), label='Password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            else:
                self.user = user  # store authenticated user for use in the view
        return cleaned_data
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist.")
        return email


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
class BookedCourseForm(forms.ModelForm):
    class Meta:
        model = BookedCourse
        fields = ['course', 'students', 'batch', 'staff']
        widgets = {
            'students': forms.Select(attrs={'class': 'form-select select2'}),
            'staff': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookedCourseForm, self).__init__(*args, **kwargs)

        self.fields['students'].queryset = User.objects.filter(role='student')
        if 'instance' in kwargs and kwargs['instance'] and kwargs['instance'].course:
            course = kwargs['instance'].course
            self.fields['staff'].queryset = course.trainers.all()
        else:
            self.fields['staff'].queryset = User.objects.filter(role='staff')
        
