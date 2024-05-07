from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def publish_status(post):
    if post.is_published:
        return format_html('<i class="fas fa-check text-success" title="Вы являетесь автором"></i>')
    return format_html('<i class="fas fa-times text-danger" title="Черновик"></i>')
