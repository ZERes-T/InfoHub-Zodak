from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """
    Преобразует обычную или короткую YouTube ссылку в embed-ссылку.
    """
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w\-]+)"
    match = re.search(pattern, url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}?rel=0"
    return ""