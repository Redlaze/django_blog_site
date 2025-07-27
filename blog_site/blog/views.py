from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post


class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class ShowPost(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    slug_url_kwarg = 'blog:post_detail'
    context_object_name = 'post'

    def get_object(self, **kwargs):
        post = get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs['post'],
            publish__year=self.kwargs['year'],
            publish__month=self.kwargs['month'],
            publish__day=self.kwargs['day'],
        )

        return post
