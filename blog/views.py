from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm

def home(req):
    context = {
        'posts':Post.objects.all(),
    }
    return render(req,'blog/home.html',context)

def about(req):
    return render(req,'blog/about.html',{'title':'About'})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/home.html'
    paginate_by = 4

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
        context['comments'] = Comment.objects.filter(post=context['post'])
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
        Comment.objects.create(text=text,post=post,author=request.user)
        messages.success(request, 'Comment added successfully!')
        return redirect('post-detail',pk=post_id)
    else:
        messages.info(request, 'cant added your comment sorry!')
    return redirect('post-detail',pk=post_id)