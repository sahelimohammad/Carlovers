from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Post , Comment ,Vote , DisLike
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm , PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# به post نیاز نداریم چون فقط نمایش اطلاعات داریم
class HomeView(View):
    form_class = PostSearchForm
    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/main_page.html', {'posts': posts , 'search':self.form_class()})

class PostDetailView(View):
    form_class = CommentCreateForm
    reply_form_class = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        can_like = False
        can_dislike = False
        if request.user.is_authenticated and self.post_instance.can_like(request.user):
            can_like = True
        elif request.user.is_authenticated and self.post_instance.can_dislike(request.user):
            can_dislike = True
        return render(request, 'home/detail.html', {'posts': self.post_instance,
                                                    'comments': comments, 'form': self.form_class(),
                                                    'can_like':can_like,'can_dislike':can_dislike,
                                                    'reply_form': self.reply_form_class()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', extra_tags='success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)

class PostDeleteView(LoginRequiredMixin, View):

    def get (self , request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post deleted successfully', extra_tags='success')
        else:
            messages.error(request, 'you cant delete this post', extra_tags='danger')
        return redirect('account:user_profile' , request.user.id)

class PostUpdateView(LoginRequiredMixin, View):
    from_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant update this post', extra_tags='danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.from_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.from_class(request.POST, request.FILES , instance=post)
        if form.is_valid():
            new = form.save(commit=False)
            new.slug = slugify(form.cleaned_data['body'][:30])
            new.save()
            messages.success(request, 'post update successfully', extra_tags='success')
            return redirect('home:post_detail', post.id, post.slug)

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST , request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.slug = slugify(form.cleaned_data['body'][:30])
            new.user = request.user
            new.save()
            messages.success(request, 'You created a new post', extra_tags='success')
            return redirect('home:post_detail', new.id, new.slug)

class CommentReplyView(LoginRequiredMixin , View):
    form_class = CommentReplyForm

    def post (self , request , post_id , comment_id):
        post = get_object_or_404(Post , id=post_id)
        comment = get_object_or_404(Comment , id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.post = post
            new.reply = comment
            new.is_reply = True
            new.save()
            messages.success(request , 'your reply submitted successfully' , extra_tags='success')
        return redirect('home:post_detail' , post.id , post.slug)

class PostLikeView (LoginRequiredMixin , View):
    def get (self , request , post_id):
        post = Post.objects.get(pk=post_id)
        like = Vote.objects.filter(post=post , user=request.user)
        if like.exists():
            messages.error(request , 'you have already liked this post' , 'danger')
        else:
            DisLike.objects.filter(post=post, user=request.user).delete()
            Vote.objects.create(post=post , user=request.user)
            messages.success(request , 'you liked this post' , 'success')
        return redirect('home:post_detail' , post.id , post.slug)

class PostDisLikeView(LoginRequiredMixin , View):
    def get (self , request , post_id):
        post = Post.objects.get(pk=post_id)
        new = DisLike.objects.filter(post=post , user=request.user)
        if new.exists():
            messages.error(request , 'you have already unliked this post' , 'danger')
        else:
            unlike = Vote.objects.filter(post=post , user=request.user)
            unlike.delete()
            DisLike.objects.create(post=post , user=request.user)
            messages.success(request, 'you unliked this post', 'success')
        return redirect('home:post_detail' , post.id , post.slug)



    
