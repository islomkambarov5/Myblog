from django import template
from blog.models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.simple_tag
def most_commented_posts():
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:5]

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
