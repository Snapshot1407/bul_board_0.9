from django import template
from apps.models import Category, Post


register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('apps/tags/last_post.html')
def get_last_post(count=5):
    posts = Post.objects.order_by("id")[:count]
    return {"last_post": posts}
