from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('category/<str:slug>/', views.category_list, name='category_list'),
    path('about/', views.about, name='about'),
    path('categories/', views.all_categories, name='all_categories'),
    path('my-articles/', views.my_articles, name='my_articles'),
    path('article/<str:slug>/edit/', views.edit_post, name='edit_post'),
    path('reviews/', views.article_review_list, name='article_review_list'),
    path('reviews/<str:slug>/', views.article_review_detail, name='article_review_detail'),
]
