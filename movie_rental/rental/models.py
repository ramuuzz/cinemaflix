from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_year = models.IntegerField()
    description = models.TextField()
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)
    rental_price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-release_year', 'title']

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('rented', 'Rented'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('canceled', 'Canceled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='transactions')
    rental_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rental_price = models.DecimalField(max_digits=6, decimal_places=2)
    late_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
    def is_overdue(self):
        return not self.return_date and timezone.now() > self.due_date
    
    def calculate_late_fee(self):
        if not self.is_overdue() or self.return_date:
            return 0
            
        days_overdue = (timezone.now() - self.due_date).days
        daily_fee = self.rental_price * 0.1  # 10% of rental price per day
        return days_overdue * daily_fee
        
    class Meta:
        ordering = ['-rental_date']