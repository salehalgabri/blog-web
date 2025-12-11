from django.contrib import admin
from .models import College, Category, Post, Comment, PostView

@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'session_key', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'user__username', 'session_key')


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_by', 'created_at', 'is_approved', 'views')
    list_filter = ('is_approved', 'is_popular', 'is_for_students', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(is_approved=True)
    approve_posts.short_description = "اعتماد المقالات المحددة"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
