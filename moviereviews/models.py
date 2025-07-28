from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django.core.paginator import Paginator

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)

    

    def __str__(self):
        return self.title

   
    def average_rating(self):
        """Calculate average rating with one decimal place"""
        avg = self.review_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0

   
    def rating_count(self):
        """Get total number of reviews"""
        return self.review_set.count()

    def get_star_rating(self):
        """Generate star display data structure"""
        avg = self.average_rating
        full_stars = int(avg)
        has_half_star = (avg - full_stars) >= 0.5
        empty_stars = 5 - full_stars - (1 if has_half_star else 0)
        
        return {
            'full': range(full_stars),
            'half': has_half_star,
            'empty': range(empty_stars),
            'average': avg,
            'count': self.rating_count
        }

    class Meta:
        ordering = ['title']  # Default ordering

from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    text = models.TextField()  # This is the correct field name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username}"

    def save(self, *args, **kwargs):
        """Override save to ensure rating is within valid range"""
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['movie', 'user']  # One review per user per movie
        ordering = ['-created_at']  # Newest first