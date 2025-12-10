from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils.text import slugify
from django.db.models import Count
from .models import Post, Category, College
from .forms import PostForm, CommentForm, SignUpForm, Comment

def home(request):
    college = College.objects.first()
    categories = Category.objects.filter(parent=None)
    
    # Pre-fetch subcategories for tabs
    categories_with_subs = []
    for cat in categories:
        subcats = cat.subcategories.all()
        categories_with_subs.append({
            'main': cat,
            'subs': subcats,
            'posts': Post.objects.filter(category__in=[cat] + list(subcats), is_approved=True)[:4]
        })

    popular_posts = Post.objects.filter(is_approved=True).order_by('-views')[:3]
    latest_posts = Post.objects.filter(is_approved=True).order_by('-created_at')[:6]
    student_posts = Post.objects.filter(is_approved=True, is_for_students=True)[:3]

    context = {
        'college': college,
        'categories_with_subs': categories_with_subs,
        'popular_posts': popular_posts,
        'latest_posts': latest_posts,
        'student_posts': student_posts,
    }
    return render(request, 'home.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Increment views
    post.views += 1
    post.save()

    comments = post.comments.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            # Auto-generate slug from title if not provided (though model requires it, we can automate it)
            # For simplicity, we'll assume slug is handled or auto-generated. 
            # Let's auto-generate it here to be safe.
            base_slug = slugify(post.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
            post.is_approved = False # Explicitly set to False
            post.save()
            return redirect('home') # Or redirect to a "pending approval" page
    else:
        form = PostForm()
    
    return render(request, 'post_form.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Get posts for this category and its children
    subcats = category.subcategories.all()
    all_cats = [category] + list(subcats)
    posts = Post.objects.filter(category__in=all_cats, is_approved=True)
    
    return render(request, 'category_list.html', {'category': category, 'posts': posts})

def about(request):
    college = College.objects.first()
    return render(request, 'about.html', {'college': college})

def all_categories(request):
    categories = Category.objects.filter(parent=None)
    return render(request, 'all_categories.html', {'categories': categories})
