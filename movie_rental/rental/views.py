from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Movie, Transaction
from .forms import CustomUserCreationForm, MovieForm, TransactionForm

def home(request):
    # Search functionality
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) | 
            Q(director__icontains=query) | 
            Q(genre__icontains=query) | 
            Q(description__icontains=query)
        ).filter(stock__gt=0)
    else:
        movies = Movie.objects.filter(stock__gt=0)
    
    return render(request, 'rental/home.html', {'movies': movies})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid() and movie.stock > 0:
            transaction = form.save(user=request.user, movie=movie)
            messages.success(request, f"You have successfully rented '{movie.title}'")
            return redirect('user_rentals')
    else:
        form = TransactionForm()
    
    return render(request, 'rental/movie_detail.html', {'movie': movie, 'form': form})

@login_required
def user_rentals(request):
    active_rentals = Transaction.objects.filter(
        user=request.user,
        status__in=['rented', 'overdue'],
        return_date__isnull=True
    )
    
    # Check for overdue rentals
    for rental in active_rentals:
        if rental.is_overdue() and rental.status != 'overdue':
            rental.status = 'overdue'
            rental.save()
    
    rental_history = Transaction.objects.filter(
        user=request.user,
        status__in=['returned', 'canceled']
    )
    
    return render(request, 'rental/user_rentals.html', {
        'active_rentals': active_rentals,
        'rental_history': rental_history
    })

@login_required
def return_movie(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id, user=request.user)
    
    if transaction.status in ['rented', 'overdue'] and not transaction.return_date:
        transaction.return_date = timezone.now()
        transaction.status = 'returned'
        
        # Calculate late fee if applicable
        if transaction.is_overdue():
            transaction.late_fee = transaction.calculate_late_fee()
            
        transaction.save()
        
        # Update movie stock
        movie = transaction.movie
        movie.stock += 1
        movie.save()
        
        messages.success(request, f"You have successfully returned '{transaction.movie.title}'")
    
    return redirect('user_rentals')
