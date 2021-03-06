from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Post, Comment
from .forms import CommentForm, EmailPostForm

from django.core.mail import send_mail
from django.conf import settings


def about(req):
    return render(req,'about.html',{'title':'About'})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/home.html'
    paginate_by = 4

    # def get_context_data(self, *args, **kwargs):
    #     context = super(PostListView, self).get_context_data(*args, **kwargs)
    #     context['comments']

class UserPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/user_posts.html'
    paginate_by = 4

    def get_queryset(self):
        user  = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)

class PostDetailView(DetailView):
    model = Post
    # context_object_name = 'oo'
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['comments'] = Comment.objects.filter(post=context['post'], reply=None)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title','content')

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title','content')

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def add_comment(request, post_id):
    if request.method=='POST':
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get('text')
        reply_id = request.POST.get('comment_id')
        comment_qs = None
        if reply_id:
            comment_qs = Comment.objects.get(id=reply_id)
        Comment.objects.create(text=text,post=post,author=request.user,reply=comment_qs)
        messages.success(request, 'Comment added successfully!')
        return redirect('post-detail',pk=post_id)
    else:
        messages.error(request, 'Sorry something went wrong! Comment not added please try again!')
    return redirect('post-detail',pk=post_id)


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action  = request.POST.get('action')
    if post_id and action:
        try:
            post = get_object_or_404(Post, id=post_id)
            if action=='like':
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            return JsonResponse({'status':'ok','id':post.id})
        except:
            pass
    return JsonResponse({'status':'ko'})

# @login_required
# @require_POST
# def post_comment(request):
#     post_id = request.POST.get('id')
#     text = request.POST.get('text')
#     comment_form = CommentForm()
#     if post_id:
#         try:
#             post = get_object_or_404(Post, id=post_id)
#             comment = Comment.objects.create(text=text,post=post,author=request.user,reply=None)
#             comments = Comment.objects.filter(post=post,reply=None)
#             # print('added')
#             context = {
#                 'post': post,
#                 'comment_form': comment_form,
#                 'comments': comments
#             }
#             rendered = render_to_string('blog/comments.html', context=context, request=request)
#             return JsonResponse({'rendered':rendered ,'status':'ok'})
#         except:
#             pass
#     return JsonResponse({'status':'ko'})


@login_required
def share_post(request, pk):
    sent = False
    post = get_object_or_404(Post, pk=pk)
    form    = EmailPostForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        post_url = request.build_absolute_uri(post.get_absolute_url())
        sub = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'],post.title)
        msg = 'Read "{}" at {} \n\n{}\'s comments: \n{} '.format(post.title,post_url,cd['name'],cd['comment'])
        sent = send_mail(sub, msg, settings.EMAIL_HOST_USER,[cd['to']])
        if sent:
            messages.success(request,"Email sent!")
        else:
            messages.error(request, "Email not sent!")
        return redirect('blog-home')
    
    return render(request, 'blog/share_post.html',{'form':form,'post':post})

        