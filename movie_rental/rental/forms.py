from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movie, Transaction

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'director', 'genre', 'release_year', 'description', 'poster', 'rental_price', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TransactionForm(forms.ModelForm):
    rental_days = forms.IntegerField(min_value=1, max_value=30, initial=7, 
                                    help_text="Number of days to rent this movie")
    
    class Meta:
        model = Transaction
        fields = ['rental_days']
        
    def save(self, commit=True, user=None, movie=None):
        transaction = super().save(commit=False)
        transaction.user = user
        transaction.movie = movie
        transaction.rental_price = movie.rental_price
        transaction.rental_date = timezone.now()
        transaction.due_date = timezone.now() + timezone.timedelta(days=self.cleaned_data['rental_days'])
        transaction.status = 'rented'
        
        if commit:
            # Update movie stock
            movie.stock -= 1
            movie.save()
            transaction.save()
        
        return transaction