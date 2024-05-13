import bleach
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def publish_status(post):
    if post.is_published:
        return format_html('<i class="fas fa-check text-success" title="Вы являетесь автором"></i>')
    return format_html('<i class="fas fa-lock text-danger" title="Черновик"></i>')


@register.filter
def sanitize_user_input(text):
    allowed_tags = ["p", "b", "i", "u"]
    cleaned_text = bleach.clean(text, tags=allowed_tags)
    return format_html(cleaned_text)
