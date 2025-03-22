from django.contrib import admin
from .models import Movie, Transaction

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'genre', 'release_year', 'rental_price', 'stock')
    list_filter = ('genre', 'release_year')
    search_fields = ('title', 'director', 'description')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rental_date', 'due_date', 'return_date', 'status')
    list_filter = ('status', 'rental_date')
    search_fields = ('user__username', 'movie__title')
    date_hierarchy = 'rental_date'
# Register your models here.
