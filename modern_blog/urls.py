from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap, CategorySitemap, StaticViewSitemap

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),

    # إبقاء هذا السطر كاحتياط لبقية الملفات (JS/CSS)
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
