# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from calendar import month_name

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import info
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from mezzanine.blog.models import BlogCategory
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import paginate, render

from forum.forms import ForumPostModelForm

from forum.models import ForumPost


class UserFilterView(ListView):
    """
    List view that puts a ``profile_user`` variable into the context,
    which is optionally retrieved by a ``username`` urlpattern var.
    If a user is loaded, ``object_list`` is filtered by the loaded
    user. Used for showing lists of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(UserFilterView, self).get_context_data(**kwargs)
        try:
            username = self.kwargs["username"]
        except KeyError:
            profile_user = None
        else:
            users = User.objects.select_related("profile")
            lookup = {"username__iexact": username, "is_active": True}
            profile_user = get_object_or_404(users, **lookup)
            qs = context["object_list"].filter(user=profile_user)
            context["object_list"] = qs
        context["profile_user"] = profile_user
        context["no_data"] = ("Whoa, there's like, literally no data here, "
                              "like seriously, I totally got nothin.")
        return context


class ForumPostView(object):

    def get_queryset(self):
        return ForumPost.objects.published().select_related('user')


def forum_post_detail(request, slug, year=None, month=None, day=None,
                     template="forum/detail.html"):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    forum_posts = ForumPost.objects.published(for_user=request.user).select_related()
    forum_post = get_object_or_404(forum_posts, slug=slug)
    context = {"forum_post": forum_post, "editable_obj": forum_post}
    templates = [u"forum/detail_%s.html" % str(slug), template]
    return render(request, templates, context)


def forum_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="forum/list.html"):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    settings.use_editable()
    templates = []
    forum_posts = ForumPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        forum_posts = forum_posts.filter(keywords__keyword=tag)
    if year is not None:
        forum_posts = forum_posts.filter(publish_date__year=year)
        if month is not None:
            forum_posts = forum_posts.filter(publish_date__month=month)
            try:
                month = month_name[int(month)]
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        forum_posts = forum_posts.filter(categories=category)
        templates.append(u"forum/list_%s.html" %
                          str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        forum_posts = forum_posts.filter(user=author)
        templates.append(u"forum/list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    forum_posts = forum_posts.select_related("user").prefetch_related(*prefetch)
    forum_posts = paginate(forum_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"forum_posts": forum_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return render(request, templates, context)


class ForumPostCreateView(CreateView):
    template_name = 'forum/create.html'
    form_class = ForumPostModelForm
    model = ForumPost

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ForumPostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.gen_description = False
        info(self.request, "Post creado")
        return super(ForumPostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("forum_post_list")