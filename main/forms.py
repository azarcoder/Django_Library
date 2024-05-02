from django import forms
from .models import Students, Books

# for users
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class studentRegisterForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ('name', 'city', 'contact', 'email', 'photo', 'password')

class bookCreationForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ('bookId', 'bookName', 'authorName', 'images')
    
    def save(self, commit=True):
        book = super().save(commit=False)
        lending_info = self.cleaned_data.get('lending_info', None)
        book.lending_info = lending_info
        if commit:
            book.save()
        return book


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']