from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from .models import Movie, Review, User
from .forms import MovieForm, ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    movies = Movie.objects.annotate(
        average_rating=Avg('review__rating'),
        review_count=Count('review')
    )
    context = {'movies': movies}
    return render(request, 'moviereviews/home.html', context)

def movie_list(request):
    movie_list = Movie.objects.annotate(
        average_rating=Avg('review__rating'),
        review_count=Count('review')
    ).order_by('-average_rating')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        movie_list = movie_list.filter(title__icontains=query)
        messages.info(request, f'Showing results for "{query}"')

    paginator = Paginator(movie_list, 10)
    page_number = request.GET.get('page')
    
    try:
        movies = paginator.page(page_number)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'moviereviews/movie_list.html', {'movies': movies})

def movie_search(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        if not movies.exists():
            messages.warning(request, f'No movies found for "{query}"')
    else:
        movies = Movie.objects.none()
        messages.info(request, 'Please enter a search term')
    
    return render(request, 'moviereviews/movie_search.html', {
        'movies': movies,
        'query': query
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'moviereviews/signup.html', {'form': form})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            messages.success(request, 'Movie added successfully!')
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm()
    return render(request, 'moviereviews/add_movie.html', {'form': form})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie.objects.annotate(
        average_rating=Avg('review__rating'),
        review_count=Count('review')
    ), pk=movie_id)
    
    reviews = movie.review_set.select_related('user').all()
    return render(request, 'moviereviews/movie_detail.html', {
        'movie': movie,
        'reviews': reviews
    })



@login_required
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Check if review already exists
    if Review.objects.filter(movie=movie, user=request.user).exists():
        messages.error(request, "You've already submitted a review for this movie!")
        return redirect('movie_detail', movie_id=movie.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    
    return render(request, 'moviereviews/add_review.html', {
        'form': form,
        'movie': movie
    })

def leaderboard(request):
    top_users = User.objects.annotate(
        review_count=Count('review'),
        average_rating=Avg('review__rating')
    ).filter(review_count__gt=0).order_by('-average_rating')[:10]
    
    return render(request, 'moviereviews/leaderboard.html', {
        'top_users': top_users
    })
def movie_search(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return redirect('movie_list')
    
    # Safest approach - use values() to get only specific fields
    movies = Movie.objects.filter(
        title__icontains=query
    ).values(
        'id', 'title', 'release_date', 'genre'
    )[:20]
    
    return render(request, 'moviereviews/movie_search.html', {
        'movies': movies,
        'query': query,
        'results_count': len(movies)
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Movie, Review

"""@login_required
def review_create(request):
    all_movies = Movie.objects.all().order_by('title')
    
    if request.method == 'POST':
        # Get form data
        movie_id = request.POST.get('movie_id')
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text', '').strip()
        
        # Validate data
        errors = []
        if not movie_id:
            errors.append("Please select a movie")
        if not rating:
            errors.append("Please provide a rating")
        if not review_text:
            errors.append("Review text cannot be empty")
        
        if errors:
            return render(request, 'reviews/review_form.html', {
                'all_movies': all_movies,
                'errors': errors,
                'preserved_data': {
                    'movie_id': movie_id,
                    'rating': rating,
                    'review_text': review_text
                }
            })
        
        try:
            # Validate rating is between 1-5
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValidationError("Rating must be between 1 and 5")
            
            # Create and save review
            Review.objects.create(
                movie_id=movie_id,
                user=request.user,
                rating=rating,
                text=review_text
            )
            return redirect('movie_list')  # Redirect to movie list after success
            
        except (ValueError, ValidationError) as e:
            errors.append(f"Invalid rating: {str(e)}")
            return render(request, 'reviews/review_form.html', {
                'all_movies': all_movies,
                'errors': errors,
                'preserved_data': {
                    'movie_id': movie_id,
                    'rating': rating,
                    'review_text': review_text
                }
            })
        except Exception as e:
            errors.append(f"Error saving review: {str(e)}")
            return render(request, 'reviews/review_form.html', {
                'all_movies': all_movies,
                'errors': errors,
                'preserved_data': {
                    'movie_id': movie_id,
                    'rating': rating,
                    'review_text': review_text
                }
            })
    
    # GET request - show empty form
    return render(request, 'reviews/review_form.html', {
        'all_movies': all_movies
    })"""