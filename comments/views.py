from django.http import Http404
from django.shortcuts import redirect

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from django.views.generic import CreateView, DetailView, TemplateView

from comments.models import Blog, Comment
from comments.forms import BlogForm, CommentForm


class MainView(TemplateView):
    template_name = "comments/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context["blog_list"] = Blog.objects.all()
        context["comments_list"] = Comment.objects.annotate(comments_count=Count("blog_id"))
        return context


class NewRecord(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "comments/blog.html"

    def get_context_data(self, **kwargs):
        context = super(NewRecord, self).get_context_data()
        return context

    def form_valid(self, form):
        if form.is_valid:
            self.record = form.save()
            return redirect("main")
        return super().form_valid(form)


class CheckComments(DetailView, CreateView):
    model = Comment
    template_name = "comments/comments.html"
    form_class = CommentForm

    def get_object(self, **kwargs):
        try:
            blog = Blog.objects.get(id=self.kwargs['id'])
        except ObjectDoesNotExist:
            raise Http404
        return blog

    def get_context_data(self, form=None, **kwargs):
        context = super(CheckComments, self).get_context_data(**kwargs)
        context["form"] = form or self.form_class()
        context["comments"] = Comment.objects.filter(blog_id=self.kwargs["id"])
        return context

    def form_valid(self, form, **kwargs):
        form.instance.blog_id = self.kwargs["id"]
        self.object = form.save()
        return redirect("check_comments", self.kwargs["id"])
