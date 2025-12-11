from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class College(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم الكلية")
    description = models.TextField(verbose_name="الوصف")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "الكلية"
        verbose_name_plural = "الكليات"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="الرابط المختصر")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name="التصنيف الأب")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="أيقونة")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "تصنيف"
        verbose_name_plural = "تصنيفات"

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان المقال")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="الرابط المختصر")
    content = models.TextField(verbose_name="المحتوى")
    excerpt = models.TextField(max_length=500, verbose_name="مقتطف")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name="التصنيف")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="الكاتب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")
    views = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")
    is_popular = models.BooleanField(default=False, verbose_name="شائع")
    is_for_students = models.BooleanField(default=False, verbose_name="موجه للطلاب")
    is_approved = models.BooleanField(default=False, verbose_name="معتمد للنشر")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "مقال"
        verbose_name_plural = "مقالات"
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="المقال")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="المستخدم")
    content = models.TextField(verbose_name="التعليق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التعليق")

    def __str__(self):
        return f"تعليق بواسطة {self.user.username} على {self.post.title}"

    class Meta:
        verbose_name = "تعليق"
        verbose_name_plural = "تعليقات"
        ordering = ['-created_at']

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_views', verbose_name="المقال")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='post_views', verbose_name="المستخدم")
    session_key = models.CharField(max_length=40, verbose_name="مفتاح الجلسة", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ المشاهدة")

    def __str__(self):
        return f"محاولة مشاهدة {self.post.title}"

    class Meta:
        verbose_name = "مشاهدة"
        verbose_name_plural = "مشاهدات"
