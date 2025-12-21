import os
import django
from django.conf import settings
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.sitemaps import Sitemap

# Set up Django environment manually
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modern_blog.settings')
django.setup()

# Now import the project modules
from blog.sitemaps import PostSitemap, CategorySitemap, StaticViewSitemap
from blog.models import Post, Category, Status

def test_sitemaps():
    print("Testing Sitemaps...")
    
    # 1. Test StaticViewSitemap
    print("\n--- StaticViewSitemap ---")
    static_sitemap = StaticViewSitemap()
    items = static_sitemap.items()
    print(f"Items: {items}")
    for item in items:
        try:
            loc = static_sitemap.location(item)
            print(f"  {item} -> {loc}")
        except Exception as e:
            print(f"  [ERROR] {item}: {e}")

    # 2. Test CategorySitemap
    print("\n--- CategorySitemap ---")
    cat_sitemap = CategorySitemap()
    cats = cat_sitemap.items()
    print(f"Found {cats.count()} categories.")
    if cats.exists():
        cat = cats.first()
        print(f"  Sample Category: {cat} -> {cat.get_absolute_url()}")
    else:
        print("  No categories found to test URL resolution.")

    # 3. Test PostSitemap (Regression check)
    print("\n--- PostSitemap ---")
    post_sitemap = PostSitemap()
    posts = post_sitemap.items()
    print(f"Found {posts.count()} approved posts.")
    if posts.exists():
        post = posts.first()
        print(f"  Sample Post: {post} -> {post.get_absolute_url()}")

if __name__ == "__main__":
    try:
        test_sitemaps()
    except Exception as e:
        print(f"FAILED: {e}")
