import re
import os
from django.conf import settings
from urllib.parse import unquote

def get_all_media_paths_from_content(html_content):
    """
    Extracts local image and file paths from HTML content.
    Returns a list of absolute file paths to the files.
    """
    if not html_content:
        return []

    # Regex to find <img src="..."> AND <a href="...">
    src_tags = re.findall(r'<img [^>]*src="([^"]+)"', html_content)
    href_tags = re.findall(r'<a [^>]*href="([^"]+)"', html_content)
    
    # Combine both lists
    all_urls = src_tags + href_tags
    
    paths = []
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT

    for url in all_urls:
        # We only care about files stored locally in MEDIA_ROOT
        if url.startswith(media_url):
            # Remove MEDIA_URL prefix to get relative path
            relative_path = url.replace(media_url, '', 1)
            # Decode URL (e.g., %20 to space)
            relative_path = unquote(relative_path)
            # Construct full path
            full_path = os.path.join(media_root, relative_path)
            
            paths.append(full_path)
            
            # Special check for thumbnails if it's an image
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            if full_path.lower().endswith(image_extensions):
                 # Insert _thumb before the extension
                 base, ext = os.path.splitext(full_path)
                 copy_image = f"{base}_thumb{ext}"
                 paths.append(copy_image)
    
    return paths

def delete_file_if_exists(path):
    """
    Deletes a file if it exists.
    """
    if os.path.isfile(path):
        try:
            os.remove(path)
            return True
        except OSError:
            pass
    return False
