from __future__ import unicode_literals
from datetime import datetime

from django.db.models import Count, Q

from mezzanine.blog.forms import BlogPostForm
from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.generic.models import Keyword
from mezzanine import template
from mezzanine.utils.models import get_user_model
from forum.models import ForumPost

User = get_user_model()

register = template.Library()


@register.as_tag
def forum_months(*args):
    """
    Put a list of dates for blog posts into the template context.
    """
    dates = ForumPost.objects.published().values_list("publish_date", flat=True)
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]["post_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def forum_categories(*args):
    """
    Put a list of categories for blog posts into the template context.
    """
    posts = ForumPost.objects.published()
    categories = BlogCategory.objects.filter(forumposts__in=posts)
    return list(categories.annotate(post_count=Count("forumposts")))


@register.as_tag
def forum_authors(*args):
    """
    Put a list of authors (users) for blog posts into the template context.
    """
    forum_posts = ForumPost.objects.published()
    authors = User.objects.filter(forumposts__in=forum_posts)
    return list(authors.annotate(post_count=Count("forumposts")))


@register.as_tag
def forum_recent_posts(limit=5, tag=None, username=None, category=None):
    """
    Put a list of recently published blog posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% blog_recent_posts 5 as recent_posts %}
        {% blog_recent_posts limit=5 tag="django" as recent_posts %}
        {% blog_recent_posts limit=5 category="python" as recent_posts %}
        {% blog_recent_posts 5 username=admin as recent_posts %}

    """
    forum_posts = ForumPost.objects.published().select_related("user")
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            forum_posts = forum_posts.filter(keywords__keyword=tag)
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = BlogCategory.objects.get(title_or_slug(category))
            forum_posts = forum_posts.filter(categories=category)
        except BlogCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            forum_posts = forum_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(forum_posts[:limit])