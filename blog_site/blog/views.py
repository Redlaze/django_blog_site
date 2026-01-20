from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from .forms import EmailPostForm
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


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        pk=post_id,
        status=Post.Status.PUBLISHED,
    )

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} рекомендует прочитать статью "{}"'.format(cd['name'], post.title)
            message = 'Читать "{}": {}\n\nКомментарий поста от {}: {}'.format(
                post.title,
                post_url,
                cd['name'],
                cd['comments'],
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[cd['to']],
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent,
        },
    )
