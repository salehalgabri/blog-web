from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post
from .utils import get_all_media_paths_from_content, delete_file_if_exists

@receiver(post_delete, sender=Post)
def cleanup_post_content_files(sender, instance, **kwargs):
    """
    Deletes all images and files embedded in the content when a Post is deleted.
    """
    content_file_paths = get_all_media_paths_from_content(instance.content)
    content_file_paths = get_all_media_paths_from_content(instance.content)
    for path in content_file_paths:
        delete_file_if_exists(path)

from django.db.models.signals import pre_save

@receiver(pre_save, sender=Post)
def cleanup_pre_save_content_files(sender, instance, **kwargs):
    """
    Deletes files removed from the content during an edit.
    """
    if not instance.pk:
        return False

    try:
        old_post = Post.objects.get(pk=instance.pk)
    except Post.DoesNotExist:
        return False

    if old_post.content != instance.content:
        # Get paths from both versions
        old_paths = set(get_all_media_paths_from_content(old_post.content))
        new_paths = set(get_all_media_paths_from_content(instance.content))
        
        # Identify files present in old but missing in new (Deleted files)
        deleted_paths = old_paths - new_paths
        
        for path in deleted_paths:
            delete_file_if_exists(path)
